import typer
# Assume your scraping function is defined here or imported
from scraper import scrape_job_post
from util import get_output_path, save_to_sheet 


app = typer.Typer()

@app.command()
def run_tracker(default: bool = typer.Option(True, help="Use current directory as default location.")):
    print("--- 🤖 Job Tracker Initialized ---")
    
    # STEP 1: Get Directory Choice (This is where you'd prompt the user)
    # For simplicity here, we will assume a placeholder path for demonstration.
    target_dir = get_output_path(default, None) # Placeholder logic
    print(f"Saving data to directory: {target_dir}")

    while True:
        try:
            # STEP 3: Get Input Link
            job_url = typer.prompt("\nEnter Job URL (or press Ctrl+C to exit):")
            
            if not job_url:
                break # Exit loop if user just hits enter without quitting
            
            print("\n🔍 Scraping data... This may take a moment.")
            # --- CORE EXECUTION ---
            extracted_data = scrape_job_post(job_url) 
            # The scraper returns a dictionary matching the required fields:
            # {'Job Title': '...', 'Company Name': '...', ...}

            if extracted_data:
                print("✨ Data extracted successfully!")
                # STEP 2 & 4: Save data
                save_to_sheet(target_dir, extracted_data)
            else:
                 typer.echo("❌ Could not extract meaningful data from this URL.")

        except KeyboardInterrupt:
            # This catches CTRL+C gracefully (Step 5 exit condition)
            print("\n\n👋 Exiting Job Tracker. Goodbye!")
            break
        except Exception as e:
            typer.echo(f"\n🚨 An unexpected error occurred: {e}")

if __name__ == "__main__":
    app()
