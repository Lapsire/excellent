import pandas as pd

class RagChunker:
    """ Vectorize chunks for a DB. """
    def flatten(self, df, metadata, initial_cat):
        chunks = []
        current_cat = initial_cat
        
        for idx, row in df.iterrows():
            # Detect category shift
            vals = [str(v).strip() for v in row.values if pd.notna(v) and str(v).strip()]
            if len(vals) == 1 and not vals[0].replace('.','').isdigit():
                current_cat = vals[0]
                continue
            
            # Build text
            data_str = "\n".join([f"{col} : {val}" for col, val in row.items() if pd.notna(val)])
            content = f"File: {metadata['file']} | Category: {current_cat}\n{data_str}"
            
            chunks.append({"content": content, "metadata": {**metadata, "category": current_cat}})
        return chunks