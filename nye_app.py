import streamlit as st
import pandas as pd
import json
import requests
from datetime import datetime
from github import Github
from github import Auth

# Data for the Airbnb listings
airbnb_data = [
    {
        "name": "Docksology | Log Cabin Retreat | Sleeps 21",
        "location": "Bracey",
        "beds": 13,
        "bedrooms": 6,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 589,
        "total_price": 3103,
        "rating": None,
        "url": "https://www.airbnb.com/rooms/1161073077086556450?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896663084&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3hE-wi0LYrPEVLM&previous_page_section_name=1000"
    },
    {
        "name": "Portside Villa Luxury Rental on Lake Gaston",
        "location": "Bracey",
        "beds": 9,
        "bedrooms": 6,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 788,
        "total_price": 4051,
        "rating": 4.0,
        "url": "https://www.airbnb.com/rooms/893413024840863979?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896655313&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3qUiMJGJPWD6bch&previous_page_section_name=1000"
    },
    {
        "name": "Dock Holiday | Magnificent Main Lake Views | Hot T",
        "location": "Littleton",
        "beds": 8,
        "bedrooms": 5,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 901,
        "total_price": 4625,
        "rating": None,
        "url": "https://www.airbnb.com/rooms/1151647794440678987?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896648770&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3IjUXVCuUjpJyNs&previous_page_section_name=1000"
    },
    {
        "name": "STUNNING VIEWS ON MAIN LAKE IN PRIVATE COMMUNITY",
        "location": "Littleton",
        "beds": 14,
        "bedrooms": 7,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 875,
        "total_price": 4394,
        "rating": 5.0,
        "tags": ["Guest favorite"],
        "url": "https://www.airbnb.com/rooms/53736420?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896643110&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3BmREUQfJDbO0Ef&previous_page_section_name=1000"
    },
    {
        "name": "Lakefront, Family/Pet Friendly, Fun for Everyone",
        "location": "Henrico",
        "beds": 13,
        "bedrooms": 7,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 750,
        "total_price": 3909,
        "rating": 5.0,
        "tags": ["Guest favorite"],
        "url": "https://www.airbnb.com/rooms/683309499174337933?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896636366&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P363FQMWnh6TxN9l&previous_page_section_name=1000"
    },
    {
        "name": "Point Breeze-Lake Anna Private Side Waterfront",
        "location": "Mineral",
        "beds": 13,
        "bedrooms": 6,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 765,
        "total_price": 4324,
        "rating": None,
        "tags": ["New place to stay"],
        "url": "https://www.airbnb.com/rooms/1187810696869244555?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896629143&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3omcOHhlT4LQW4W&previous_page_section_name=1000"
    },
    {
        "name": "Multi-family DREAM. Sleeps 20 w/ 2 full kitchens",
        "location": "Bumpass",
        "beds": 13,
        "bedrooms": 6,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 1000,
        "total_price": 5249,
        "rating": 5.0,
        "tags": ["Guest favorite"],
        "url": "https://www.airbnb.com/rooms/968145862476252827?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003888756938&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723683197_P33zUoo1div0gbHQ&previous_page_section_name=1000"
    },
    {
        "name": "7BR Lakefront | Chef's Kitchen| Hot Tub | Dock",
        "location": "Bumpass",
        "beds": 19,
        "bedrooms": 7,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 982,
        "total_price": 5018,
        "rating": 4.87,
        "url": "https://www.airbnb.com/rooms/29736526?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003888756378&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723683197_P3wGI_hkc4b3SSyf&previous_page_section_name=1000"
    },
    {
        "name": "Family Reunion Shenandoah Oasis",
        "location": "Stanley",
        "beds": 8,
        "bedrooms": 7,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 950,
        "total_price": 4593,
        "rating": None,
        "tags": ["Superhost"],
        "url": "https://www.airbnb.com/rooms/903347714847652967?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003888739177&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723683197_P3GnkpU3noTSovke&previous_page_section_name=1000"
    }]


# Airbnb data stored directly in the script
airbnb_data = [
    {
        "name": "Docksology | Log Cabin Retreat | Sleeps 21",
        "location": "Bracey",
        "beds": 13,
        "bedrooms": 6,
        "nights": 4,
        "dates": "Dec 28 – Jan 1",
        "price_per_night": 589,
        "total_price": 3103,
        "rating": None,
        "url": "https://www.airbnb.com/rooms/1161073077086556450?adults=16&children=0&infants=0&pets=0&wishlist_item_id=11003896663084&check_in=2024-12-28&check_out=2025-01-01&source_impression_id=p3_1723682858_P3hE-wi0LYrPEVLM&previous_page_section_name=1000"
    },
    # ... Add all other Airbnb listings here ...
]

# GitHub configuration
GITHUB_TOKEN = st.secrets["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"]
REPO_NAME = "finnman81/weekly_progress_app"
VOTES_FILE = "votes_data.json"
COMMENTS_FILE = "comments_data.json"

auth = Auth.Token(GITHUB_TOKEN)
g = Github(auth=auth)
repo = g.get_repo(REPO_NAME)

@st.cache_data(ttl=600)  # Cache for 10 minutes
def load_github_data(file_name):
    try:
        content = repo.get_contents(file_name)
        data = json.loads(content.decoded_content.decode())
        return data
    except Exception as e:
        st.error(f"Error loading data from GitHub: {str(e)}")
        return []

def save_github_data(file_name, data):
    try:
        content = repo.get_contents(file_name)
        repo.update_file(
            path=file_name,
            message=f"Update {file_name}",
            content=json.dumps(data, indent=2),
            sha=content.sha
        )
    except Exception as e:
        st.error(f"Error saving data to GitHub: {str(e)}")

def save_vote(user_name, user_email, listing_name):
    votes_data = load_github_data(VOTES_FILE)
    votes_data.append({
        "user_name": user_name,
        "user_email": user_email,
        "listing_name": listing_name,
        "timestamp": datetime.now().isoformat()
    })
    save_github_data(VOTES_FILE, votes_data)
    st.cache_data.clear()
    return votes_data

def save_comment(user_name, user_email, listing_name, comment):
    comments_data = load_github_data(COMMENTS_FILE)
    comments_data.append({
        "user_name": user_name,
        "user_email": user_email,
        "listing_name": listing_name,
        "comment": comment,
        "timestamp": datetime.now().isoformat()
    })
    save_github_data(COMMENTS_FILE, comments_data)
    st.cache_data.clear()
    return comments_data

def main():
    st.title("BPM 2025 NYE Extravaganza Airbnb Selection")
    st.write("Help choose the perfect Airbnb for our group!")

    user_name = st.text_input("Your Name")
    user_email = st.text_input("Your Email")

    if not user_name or not user_email:
        st.warning("Please enter your name and email to vote or comment.")
        return

    votes_data = load_github_data(VOTES_FILE)
    comments_data = load_github_data(COMMENTS_FILE)

    user_votes = sum(1 for vote in votes_data if vote["user_email"] == user_email)
    votes_left = 3 - user_votes

    st.write(f"You have {votes_left} votes left.")

    for listing in airbnb_data:
        st.subheader(listing['name'])
        st.write(f"Location: {listing['location']}")
        st.write(f"Beds: {listing['beds']}, Bedrooms: {listing['bedrooms']}")
        st.write(f"Price per night: ${listing['price_per_night']}")
        st.write(f"Total price: ${listing['total_price']}")
        if listing['rating']:
            st.write(f"Rating: {listing['rating']} out of 5")
        if 'tags' in listing and listing['tags']:
            st.write(f"Tags: {', '.join(listing['tags'])}")
        st.write(f"[View on Airbnb]({listing['url']})")
        
        # Voting
        if votes_left > 0:
            if st.button(f"Vote for {listing['name']}"):
                votes_data = save_vote(user_name, user_email, listing['name'])
                st.success("Vote recorded!")
                votes_left -= 1
        
        # Display vote count for this listing
        listing_votes = sum(1 for vote in votes_data if vote["listing_name"] == listing['name'])
        st.write(f"Total votes: {listing_votes}")
        
        # Comments
        comment = st.text_input(f"Comment on {listing['name']}")
        if comment:
            comments_data = save_comment(user_name, user_email, listing['name'], comment)
            st.success("Comment recorded!")
        
        # Display comments for this listing
        listing_comments = [comment for comment in comments_data if comment["listing_name"] == listing['name']]
        if listing_comments:
            st.write("Comments:")
            for comment in listing_comments:
                st.write(f"- {comment['user_name']}: {comment['comment']}")
        
        st.write("---")

    # Display overall voting results
    st.subheader("Current Voting Results")
    vote_counts = pd.DataFrame(votes_data)['listing_name'].value_counts()
    st.bar_chart(vote_counts)

if __name__ == "__main__":
    main()
