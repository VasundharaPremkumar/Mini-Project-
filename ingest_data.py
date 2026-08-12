import pandas as pd
import asyncio
from database import crimes_collection, ncrb_collection

async def ingest_chicago_crimes():
    print("Ingesting Chicago Crimes sample...")
    df = pd.read_csv(r"c:\Users\Lenovo\Desktop\crime data\chicago crimes.csv", nrows=50000)
    df = df.dropna(subset=['Latitude', 'Longitude', 'Primary Type'])
    
    records = []
    for _, row in df.iterrows():
        records.append({
            "case_number": row.get("Case Number"),
            "date": row.get("Date"),
            "crime_type": row.get("Primary Type"),
            "description": row.get("Description"),
            "location_desc": row.get("Location Description"),
            "latitude": row.get("Latitude"),
            "longitude": row.get("Longitude"),
        })
    
    await crimes_collection.delete_many({})
    if records:
        chunk_size = 1000
        for i in range(0, len(records), chunk_size):
            await crimes_collection.insert_many(records[i:i+chunk_size])
    print(f"Chicago Crimes ingestion complete: {len(records)} records inserted.")

async def ingest_ncrb_data():
    print("Ingesting NCRB State data...")
    df = pd.read_csv(r"c:\Users\Lenovo\Desktop\crime data\NCRB_Table_1A.1.csv", header=0)
    
    # Check headers and extract data
    # Columns are like: Sl. No.,State/UT,2020,2021,2022,Mid-Year Projected...
    records = []
    for _, row in df.iterrows():
        state = row.get("State/UT")
        if pd.isna(state) or state.startswith("Total"): 
            continue
        
        # safely handle strings that might not cast cleanly, although given the sample they are mostly ints
        try:
            val_2022 = float(row.get("2022", 0))
            pop = float(row.get("Mid-Year Projected Population (in Lakhs) (2022)", 0))
            rate = float(row.get("Rate of Cognizable Crimes (IPC) (2022)", 0))
        except:
            val_2022 = 0
            pop = 0
            rate = 0

        records.append({
            "state": state,
            "crimes_2022": val_2022,
            "population_lakhs": pop,
            "crime_rate": rate
        })

    await ncrb_collection.delete_many({})
    if records:
        await ncrb_collection.insert_many(records)
    print(f"NCRB Data ingestion complete: {len(records)} records inserted.")

async def main():
    await ingest_chicago_crimes()
    await ingest_ncrb_data()
    print("All ingestion tasks finished.")

if __name__ == "__main__":
    asyncio.run(main())
