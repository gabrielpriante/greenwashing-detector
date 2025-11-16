# Data Folder

This folder is for storing your data files for greenwashing analysis.

## Suggested Data Files

You can place the following types of files here:

- **CSV files**: Product descriptions, marketing claims, company statements
- **Text files**: Documents to analyze
- **JSON files**: Structured data about products and claims

## Example Data Structure

If you create a CSV file, consider this structure:

```csv
product_id,product_name,category,claim,source
1,Product A,Cleaning,Our eco-friendly cleaner is 100% natural,Website
2,Product B,Packaging,Made with recycled materials,Label
3,Product C,Clothing,Sustainable organic cotton,Tag
```

## Notes

- This folder is included in `.gitignore` for data files larger than needed
- Add your own `.gitkeep` or README files to track this folder in git if needed
- Make sure not to commit sensitive or proprietary data
