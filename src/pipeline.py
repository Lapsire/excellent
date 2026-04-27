import pandas as pd
from core import ExcelSegmenter, ExcelTableCleaner, RagChunker

class PipelineExtractor :
    """ Command the excel data extraction. """
    def __init__(self):
        self.segmenter = ExcelSegmenter()
        self.cleaner = ExcelTableCleaner()
        self.chunker = RagChunker()

    def run(self, filepath):
        all_chunks = []
        file_name = filepath.split('/')[-1]
        sheets = pd.read_excel(filepath, header=None, sheet_name=None)
        
        for name, df in sheets.items():
            islands = self.segmenter.get_islands(df, name, file_name)
            for island in islands:
                clean_df, first_cat = self.cleaner.clean(island['dataframe'])
                chunks = self.chunker.flatten(clean_df, island['metadata'], first_cat)
                all_chunks.extend(chunks)
        return all_chunks