# NCDIT Document Demos

This repository hosts a demonstration dataset and compliance reporting for the **North Carolina Department of Information Technology (NCDIT)**. It primarily serves the NCDIT 911 Board.

## Repository Structure

- `data/`: Contains **1,829** document folders totaling **14,443** files (approximately 8.5 GB). This includes raw PDFs, JSON metadata, Markdown representations, and HTML documents. These files are tracked using Git Large File Storage (LFS).
- `NCDIT_Compliance_Score_Report.txt`: The primary overall compliance score report detailing accessibility, structural, HTML quality, and content preservation metrics across the indexed documents.


## Compliance Report Summary

The included compliance report shows a very high standard of document quality and accessibility:
- **Compliance Rate**: 99.9% (1,794 out of 1,795 scored documents met the >=75 threshold).
- **Average Compliance Score**: 97.7 / 100.
- **Pillar Highlights**: 
  - *HTML Quality*: 0.9997
  - *Axe-Core Compliance*: 0.9961
  - *Structural Compliance*: 0.9767
  - *Content Preservation*: 0.9484

## Setup & Cloning

Because this repository utilizes Git LFS for large files in the `data/` folder, ensure you have Git LFS installed before cloning:

```bash
# Install Git LFS (macOS example)
brew install git-lfs

# Initialize LFS
git lfs install

# Clone the repository
git clone <repository-url>
```

This repository is maintained within the **GPS demos** organization.