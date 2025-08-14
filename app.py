import streamlit as st
import pandas as pd
import asyncio
from concurrent.futures import ProcessPoolExecutor
from scrapeLinkedIn.scraper import scrapeLinkedIn

# --- Helper to run scraper in a separate process ---
def run_scraper_process(role, location, data_name):
    import asyncio
    from scrapeLinkedIn.scraper import scrapeLinkedIn

    # Ensure we always return a DataFrame
    df = asyncio.run(scrapeLinkedIn(role, location, data_name))
    if df is None:
        import pandas as pd
        df = pd.DataFrame()
    return df

# --- Streamlit UI ---
st.title("LinkedIn Job Scraper & Insights")

role = st.text_input("Enter Job Role")
location = st.text_input("Enter Location")
data_name = st.text_input("Data Name (optional)", value="jobs_data")

if st.button("Run Scraper"):
    if not role or not location:
        st.warning("Please enter both role and location")
    else:
        with st.spinner("Scraping LinkedIn jobs..."):
            try:
                # Run scraper safely in a separate process
                with ProcessPoolExecutor() as executor:
                    future = executor.submit(run_scraper_process, role, location, data_name)
                    jobs_df = future.result()

                # Safety check
                if jobs_df is None or jobs_df.empty:
                    st.info("No jobs found for this search.")
                else:
                    st.success(f"Found {len(jobs_df)} jobs!")
                    st.dataframe(jobs_df)

                    # --- Insights ---
                    st.markdown("### Key Insights")

                    # Top Companies
                    if 'Company' in jobs_df.columns:
                        company_counts = jobs_df['Company'].value_counts().head(5)
                        st.subheader("Top Companies")
                        st.bar_chart(company_counts)

                    # Top Locations
                    if 'Location' in jobs_df.columns:
                        location_counts = jobs_df['Location'].value_counts().head(5)
                        st.subheader("Top Locations")
                        st.bar_chart(location_counts)

                    # Summary Metrics
                    st.subheader("Summary Metrics")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Jobs", len(jobs_df))
                    col2.metric("Unique Companies", jobs_df['Company'].nunique() if 'Company' in jobs_df.columns else 0)
                    col3.metric("Unique Locations", jobs_df['Location'].nunique() if 'Location' in jobs_df.columns else 0)

            except Exception as e:
                st.error(f"Error running scraper: {e}")
