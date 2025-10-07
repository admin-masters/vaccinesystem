import pandas as pd

def check_education_excel():
    print("Checking education.xlsx structure...")
    
    try:
        excel_file = "education.xlsx"
        
        # Get all sheet names
        xl_file = pd.ExcelFile(excel_file)
        print(f"Sheet names: {xl_file.sheet_names}")
        
        # Check PE sheet
        if 'PE' in xl_file.sheet_names:
            print(f"\n=== PE Sheet ===")
            pe_df = pd.read_excel(excel_file, sheet_name='PE')
            print(f"Columns: {list(pe_df.columns)}")
            print(f"Rows: {len(pe_df)}")
            if len(pe_df) > 0:
                print(f"First row data:")
                for col in pe_df.columns:
                    print(f"  {col}: {pe_df.iloc[0][col]}")
        
        # Check DE sheet
        if 'DE' in xl_file.sheet_names:
            print(f"\n=== DE Sheet ===")
            de_df = pd.read_excel(excel_file, sheet_name='DE')
            print(f"Columns: {list(de_df.columns)}")
            print(f"Rows: {len(de_df)}")
            if len(de_df) > 0:
                print(f"First row data:")
                for col in de_df.columns:
                    print(f"  {col}: {de_df.iloc[0][col]}")
        
        # If PE/DE don't exist, check what sheets are available
        for sheet_name in xl_file.sheet_names:
            if sheet_name not in ['PE', 'DE']:
                print(f"\n=== {sheet_name} Sheet ===")
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                print(f"Columns: {list(df.columns)}")
                print(f"Rows: {len(df)}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_education_excel()
