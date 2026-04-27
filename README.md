# Excellent-RAG

**Extract and prepare messy, human-made Excel files for Retrieval-Augmented Generation (RAG) pipelines.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Standard document loaders often fail when dealing with real-world corporate Excel files. Human-made spreadsheets are rarely clean databases; they contain multiple scattered tables, merged cells, fake titles, and empty rows used for spacing. 

**Excellent-RAG** solves this by using a density-based algorithm to detect data "Islands", clean their headers, and flatten the data into LLM-friendly textual chunks with precise metadata. It runs 100% locally using Pandas, keeping your sensitive financial or HR data secure.

## Features

* **Island Detection:** Automatically isolates multiple disconnected tables on a single Excel sheet based on a configurable data density threshold.
* **Intelligent Header Cleaning:** Identifies true headers by penalizing numerical rows, handling merged-like empty cells perfectly.
* **Context Preservation:** Captures category titles (e.g., isolated text cells or uppercase titles) and injects them into the metadata of every chunk.
* **RAG-Ready Output:** Flattens rows into `Column : Value` formats, generating chunks ready to be embedded into any Vector Database (Qdrant, Pinecone, ChromaDB).

## Quick Start

Extracting data from a messy Excel file is as simple as running the `PipelineExtractor`:

```python
from excellent.pipeline import PipelineExtractor

# Initialize the pipeline
extractor = PipelineExtractor()

# Run the extraction on your messy Excel file
chunks = extractor.run("data/messy_financial_report.xlsx")

# Print the first extracted chunk
print(chunks[0])
```

### Output Format
The pipeline outputs a list of dictionaries, perfectly formatted for your vector database payloads:

```json
{
  "content": "File: messy_financial_report.xlsx | Category: Q3 EXPENSES\nDate : 2023-09-15\nDescription : Server Hosting\nAmount : 450.00",
  "metadata": {
    "sheet": "Sheet1",
    "file": "messy_financial_report.xlsx",
    "category": "Q3 EXPENSES"
  }
}
```

## How It Works (Under the Hood)

The pipeline is divided into three core components:
1. **`ExcelSegmenter`**: Scans the sheet and groups adjacent non-empty cells into distinct DataFrames ("Islands"), filtering out noise using a minimum density threshold.
2. **`ExcelTableCleaner`**: Analyzes each island to find the most probable header row, fixes missing column names, and extracts overarching categories.
3. **`RagChunker`**: Iterates through the cleaned data, drops empty values, and builds dense, highly contextualized text chunks.

## Contributing
Contributions, issues, and feature requests are welcome!

## License
This project is licensed under the MIT License - see the LICENSE file for details.