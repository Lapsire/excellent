import pandas as pd

class ExcelTableCleaner:
    """ Clean islands : find header, manage types and false titles. """
    def __init__(self, search_depth=5):
        # Size of the area we'll search the header on the island
        self.search_depth = search_depth

    def _is_numeric(self, val):
        if pd.isna(val): return False
        s = str(val).replace(' ', '').replace('%', '').replace(',', '.')
        try:
            float(s)
            return True
        except:
            return False

    def clean(self, island_df):
        df = island_df.reset_index(drop=True)
        best_score, header_idx = -999, 0

        # Scoring algorithm
        for i in range(min(self.search_depth, len(df))):
            row = df.iloc[i]
            score = row.notna().sum() - (sum(1 for v in row if self._is_numeric(v)) * 5)
            if score > best_score:
                best_score, header_idx = score, i

        # Rebuilding column
        new_cols = []
        for col_idx, val in enumerate(df.iloc[header_idx]):
            val_str = str(val).strip()
            if val_str.lower() in ['nan', '', 'none']:
                # We look on the line above for the merged titles
                val_above = df.iloc[header_idx-1, col_idx] if header_idx > 0 else None
                new_cols.append(str(val_above) if pd.notna(val_above) else f"Column_{col_idx+1}")
            else:
                new_cols.append(val_str)


        # Extract category
        initial_cat = None
        if len(df.columns) > 1:
            val_col_1 = str(df.iloc[header_idx, 0]).strip().lower()
            val_col_2 = str(df.iloc[header_idx, 1]).strip().lower()
            
            # If case 1 have text but case 2 is empty
            if val_col_1 not in ['nan', '', 'none'] and val_col_2 in ['nan', '', 'none']:
                initial_cat = new_cols[0]  # We get the real name
                new_cols[0] = "Column_1"   # We reset the name

        df.columns = new_cols
        return df.iloc[header_idx+1:].reset_index(drop=True), initial_cat