import pandas as pd
from sklearn.neighbors import NearestNeighbors
from typing import List, Dict
from database import crimes_collection
import re

class CrimePatternMatcher:
    def __init__(self):
        self.df = None
        self.is_trained = False
        
        # General Intelligence NLP Dictionary
        self.nlp_map = {
            "murder": "HOMICIDE", "kill": "HOMICIDE", "shot": "HOMICIDE", "dead": "HOMICIDE",
            "robbed": "ROBBERY", "stole": "THEFT", "mugged": "ROBBERY", "pickpocket": "THEFT", "purse": "THEFT",
            "fight": "BATTERY", "beat up": "BATTERY", "punched": "BATTERY", "attack": "ASSAULT", "assaulted": "ASSAULT",
            "fire": "ARSON", "burn": "ARSON", "arson": "ARSON",
            "drugs": "NARCOTICS", "weed": "NARCOTICS", "meth": "NARCOTICS", "cocaine": "NARCOTICS",
            "kidnap": "KIDNAPPING", "abduct": "KIDNAPPING",
            "break in": "BURGLARY", "intruder": "BURGLARY", "trespass": "CRIMINAL TRESPASS",
            "car stolen": "MOTOR VEHICLE THEFT", "carjack": "MOTOR VEHICLE THEFT",
            "fake": "DECEPTIVE PRACTICE", "fraud": "DECEPTIVE PRACTICE", "scam": "DECEPTIVE PRACTICE"
        }

    async def load_and_train(self):
        print("Fetching data from MongoDB for Semantic ML core...")
        cursor = crimes_collection.find({})
        crimes = await cursor.to_list(length=None)
        
        if not crimes:
            print("No data available for training.")
            return False

        self.df = pd.DataFrame(crimes)
        self.df['latitude'] = self.df['latitude'].fillna(0)
        self.df['longitude'] = self.df['longitude'].fillna(0)
        
        # We no longer globally train NearestNeighbors on encoded types
        # because categorical proximity makes no geographic/semantic sense.
        # We hold the raw dataframe to build dynamic k-NN models per-query.
        self.is_trained = True
        print("Dataset loaded into memory. Ready for dynamic NLP routing.")
        return True

    def _parse_human_language(self, text: str) -> str:
        text = text.lower().strip()
        # Direct dictionary translation
        for key, official_value in self.nlp_map.items():
            if re.search(r'\b' + re.escape(key) + r'\b', text):
                return official_value
        
        # If no semantic slang is found, assume they typed the direct official term, just upper cased.
        return text.upper()

    def find_matches(self, latitude: float, longitude: float, human_query: str) -> List[Dict]:
        if not self.is_trained or self.df is None or len(self.df) == 0:
            return []
            
        # 1. NLP Translation Phase
        official_crime_type = self._parse_human_language(human_query)
        
        # 2. Strong Filter Isolation (FIx the Arson Bug)
        filtered_df = self.df[self.df['crime_type'] == official_crime_type].copy()
        
        if len(filtered_df) == 0:
            # Fallback if the user types something wholly unmapped and not strictly official
            filtered_df = self.df.copy()
            fallback = True
        else:
            fallback = False

        # 3. Dynamic Spatial Matrix
        X = filtered_df[['latitude', 'longitude']]
        k = min(20, len(X))
        if k == 0:
            return []
            
        knn = NearestNeighbors(n_neighbors=k, algorithm='ball_tree')
        knn.fit(X)
        
        query_point = [[latitude, longitude]]
        distances, indices = knn.kneighbors(query_point)
        
        matches = []
        for i in range(len(indices[0])):
            idx = indices[0][i]
            dist = distances[0][i]
            matched_row = filtered_df.iloc[idx]
            
            match_type = matched_row.get("crime_type", "Unknown")
            match_desc = matched_row.get("description", "Unknown")
            match_year = str(matched_row.get("date", "Unknown"))[:4]
            score_percent = round((1 / (1 + dist)) * 100, 1)

            if score_percent < 50.0:
                continue

            # Generate conversational AI suggestion
            if not fallback:
                if score_percent > 90:
                    ai_suggestion = f"Critical Spatial Link. This '{human_query}' occurred exactly where a historic {match_year} {match_type} took place. Review local CCTV timelines."
                elif score_percent > 70:
                    ai_suggestion = f"Pattern Similarity Detected. The coordinates isolate a previous {match_desc} ({match_type}) incident from {match_year} nearby."
                else:
                    ai_suggestion = f"Sector Match. This area has seen {match_type} occurrences historically, mirroring your query '{human_query}'."
            else:
                ai_suggestion = f"Warning: Exact classification unmapped. Showing closest general geographic anomaly: {match_type}."

            matches.append({
                "case_number": matched_row.get("case_number", "Unknown"),
                "date": matched_row.get("date", "Unknown"),
                "crime_type": match_type,
                "description": match_desc,
                "location_desc": matched_row.get("location_desc", "Unknown"),
                "similarity_score": round(1 / (1 + dist), 4),
                "latitude": matched_row.get("latitude"),
                "longitude": matched_row.get("longitude"),
                "ai_suggestion": ai_suggestion
            })
            
        return matches

# Singleton instance
ml_matcher = CrimePatternMatcher()
