class ExcelSegmenter:
    """ Isolate the differents islands of a Excel. """
    def __init__(self, min_density=0.3):
        # Density : minimum of rows that needs to be filled to validate an island
        self.min_density = min_density

    def get_islands(self, df, sheet_name, file_name):
        islands = []

        # Drop a row if empty (trim the excel)
        df = df.dropna(how='all', axis=0).reset_index(drop=True) # Drop a row if empty (trim the excel)
        if df.empty: return []
        
        # Detects the adjacents blocks
        valid_rows = df.notna().any(axis=1)
        valid_cols = df.notna().any(axis=0)
        row_blocks = valid_rows[valid_rows].groupby((~valid_rows).cumsum()).groups
        col_blocks = valid_cols[valid_cols].groupby((~valid_cols).cumsum()).groups

        for r_idx in row_blocks.values():
            for c_idx in col_blocks.values():
                island_df = df.loc[r_idx, c_idx].dropna(how='all', axis=0).dropna(how='all', axis=1)
                if island_df.empty: continue
                
                # Calculate density to eliminate noise
                density = island_df.notna().sum().sum() / (island_df.shape[0] * island_df.shape[1])
                if density >= self.min_density:
                    islands.append({
                        "dataframe": island_df,
                        "metadata": {"sheet": sheet_name, "file": file_name}
                    })
        return islands