import pandas as pd

class RagChunker:
    """ Vectorize chunks for a DB. """
    def flatten(self, df, metadata, initial_cat):
        chunks = []
        current_cat = initial_cat
        
        for idx, row in df.iterrows():
            vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip() != ""]
            
            if len(vals) == 1 and not vals[0].replace('.','').isdigit():
                current_cat = vals[0]
                continue 
            
            # Category in CAP
            col_0_val = str(row.iloc[0]).strip()
            is_pure_text = col_0_val.replace(' ', '').replace('-', '').isalpha()
            if len(col_0_val) >= 2 and col_0_val.isupper() and is_pure_text:
                current_cat = col_0_val

            if not vals: continue
            
            # Kill repeted headers
            header_matches = sum(1 for c, v in row.items() if str(c).strip() == str(v).strip() and pd.notna(v))
            if header_matches >= 3: 
                col_0_name = df.columns[0]
                if pd.notna(col_0_val) and str(col_0_val).strip() != str(col_0_name).strip():
                    current_cat = str(col_0_val).strip()
                continue 
            
            valid_cells = []
            for col_name, value in row.items():
                c_name = str(col_name).replace('\n', ' ').strip()
                if pd.notna(value) and str(value).strip() != "":
                    valid_cells.append(f"{c_name} : {value}")
            
            if not valid_cells: continue
            
            # Build final text
            data_str = "\n".join(valid_cells)
            content = f"File: {metadata['file']} | Category: {current_cat}\n{data_str}"
            
            chunks.append({"content": content, "metadata": {**metadata, "category": current_cat}})
            
        return chunks