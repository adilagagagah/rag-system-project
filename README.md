# Use Case

Membangun Executive Report Assistant untuk:

Mengekstrak insight dari laporan 99 halaman
Menjawab pertanyaan berbasis dokumen
Menyajikan key points + evidence
Contoh Query Target
“Apa highlight performance bulan ini?”
“Bagaimana trend revenue wholesale?”
“Apa isu utama customer experience?”
“Bagian mana yang menjelaskan CAPEX?”
Expected Output
Jawaban ringkas (executive-style)
Dilengkapi:
kutipan sumber
halaman asal

## Flow

PDF (99 slides)
   ↓
Slide Extraction
   ↓
Slide Parsing (title + content)
   ↓
[OPTIONAL] Table-aware cleaning
   ↓
Embedding (per slide)
   ↓
Vector DB
   ↓
Retriever (top-k slides)
   ↓
LLM (summarize + answer)
   ↓
Answer + Slide Reference
>