import streamlit as st
import json
import os
import re
from datetime import datetime

from nlp_processor import analyze_food_message
from matcher import find_matches

# =========================================================
# FOOD DONOR - COMPLETE UI/UX VERSION
# Design based on the supplied Food Donor UI reference
# =========================================================

st.set_page_config(
    page_title="Food Donor",
    page_icon="🍱",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_FILE = os.path.join(BASE_DIR, "users.json")
DONATION_FILE = os.path.join(BASE_DIR, "donations.json")
ASSET_DIR = os.path.join(BASE_DIR, "assets")


# =========================================================
# TRANSLATIONS
# =========================================================

TEXT = {
    "English": {
        "food_donor": "FOOD DONOR",
        "tagline": "Good Food • Happy Life",
        "together": "Together we can end hunger.",
        "home": "Home",
        "donor": "Donate Food",
        "receiver": "Find Food",
        "language": "Language",
        "notifications": "Notifications",
        "profile": "My Profile",
        "history": "History",
        "settings": "Settings",
        "logout": "Logout",
        "dashboard": "DASHBOARD",
        "welcome": "Good food creates a better tomorrow.",
        "welcome_name": "Hello, {name} 👋",
        "share_food": "Share Food",
        "support_communities": "Support Communities",
        "better_tomorrow": "Build a Better Tomorrow",
        "donate_card": "Donate Food",
        "donate_card_text": "Share your extra food and make a difference.",
        "find_card": "Find Food",
        "find_card_text": "Discover available food near you.",
        "available_near": "Available Near You",
        "view_all": "View All →",
        "meals_helped": "Meals Donated",
        "people_helped": "People Helped",
        "food_saved": "Kg Food Saved",
        "active_donors": "Active Donors",
        "first_time_donor": "First Time Donor",
        "donor_login": "Donor Login",
        "first_time_receiver": "First Time Receiver",
        "receiver_login": "Receiver Login",
        "create_account": "Create Account",
        "login": "Login",
        "username": "User Name",
        "email": "Email",
        "phone": "Phone Number",
        "trust_code": "Trust Code",
        "welcome_back": "Welcome back! Please login to continue.",
        "first_registration": "These details are requested only during your first registration.",
        "food_photo": "Food Photo",
        "food_name": "Food Name",
        "food_category": "Food Category",
        "servings": "Servings",
        "prepared_time": "Prepared Time",
        "expiry_date": "Expiry Date",
        "pickup_location": "Pickup Location",
        "notes": "Additional Notes",
        "publish": "Publish Donation",
        "food_description": "Describe your available food",
        "analyze_find": "Analyze & Find Receivers",
        "nlp_analysis": "NLP Analysis",
        "food_type": "Food Type",
        "quantity": "Quantity",
        "urgency": "Urgency",
        "suitable": "Suitable Receivers",
        "receiver_found": "receiver(s) found",
        "no_receiver": "No suitable receiver found.",
        "find_food_title": "Find Food",
        "find_food_sub": "Discover good food near you.",
        "search": "Search food, location or donor...",
        "within": "Within 5 km",
        "all_categories": "All Categories",
        "vegetarian": "Vegetarian",
        "available_now": "Available Now",
        "request": "Request",
        "accept": "Accept Donation",
        "donated_by": "Donated by",
        "verified": "Verified Donor",
        "distance": "km",
        "language_title": "Select Language",
        "language_sub": "Choose your preferred language to continue.",
        "save_language": "Save Language",
        "notification_title": "Notifications",
        "notification_sub": "Stay updated with your food journey.",
        "new_request": "New Food Request",
        "request_accepted": "Request Accepted",
        "pickup_reminder": "Pickup Reminder",
        "donation_completed": "Donation Completed",
        "new_message": "New Message",
        "profile_title": "My Profile",
        "good_food": "Good food. Greater impact.",
        "trusted_donor": "Trusted Donor",
        "donations": "Donations",
        "people_helped": "People Helped",
        "kg_saved": "Kg Food Saved",
        "edit_profile": "Edit Profile",
        "privacy": "Privacy & Security",
        "history_title": "My Food Activity",
        "donation_tab": "Donations",
        "request_tab": "Requests",
        "no_history": "No history available.",
        "no_notifications": "No notifications yet.",
        "please_login": "Please login first.",
        "account_created": "Account created successfully!",
        "login_success": "Login successful!",
        "donation_added": "Food donation added successfully!",
        "donation_accepted": "Donation accepted successfully!",
        "donor_notified": "The donor has been notified.",
        "enter_name": "Please enter your User Name.",
        "valid_email": "Please enter a valid Email.",
        "valid_phone": "Please enter a valid 10-digit Phone Number.",
        "enter_trust": "Please enter your Trust Code.",
        "trust_used": "This Trust Code is already used.",
        "name_not_found": "User Name not found.",
        "wrong_receiver": "User Name or Trust Code is incorrect.",
        "describe_food": "Please describe the food.",
        "enter_location": "Please enter the Pickup Location.",
        "no_food": "No food donations are currently available.",
        "meals": "meals",
        "available": "Available",
        "accepted": "Accepted",
        "requested": "Requested",
        "completed": "Completed",
        "normal": "Normal",
    },
    "Tamil": {
        "food_donor": "உணவு நன்கொடையாளர்", "tagline": "நல்ல உணவு • மகிழ்ச்சியான வாழ்க்கை",
        "together": "ஒன்றாக பசியை முடிவுக்கு கொண்டு வரலாம்.", "home": "முகப்பு",
        "donor": "உணவு வழங்கு", "receiver": "உணவு தேடு", "language": "மொழி",
        "notifications": "அறிவிப்புகள்", "profile": "என் சுயவிவரம்", "history": "வரலாறு",
        "settings": "அமைப்புகள்", "logout": "வெளியேறு", "dashboard": "டாஷ்போர்டு",
        "welcome": "நல்ல உணவு சிறந்த நாளை உருவாக்குகிறது.", "welcome_name": "வணக்கம், {name} 👋",
        "share_food": "உணவை பகிருங்கள்", "support_communities": "சமூகங்களுக்கு உதவுங்கள்",
        "better_tomorrow": "சிறந்த நாளை உருவாக்குங்கள்", "donate_card": "உணவு நன்கொடை",
        "donate_card_text": "உங்கள் மீதமான உணவை பகிர்ந்து மாற்றத்தை உருவாக்குங்கள்.",
        "find_card": "உணவை தேடுங்கள்", "find_card_text": "உங்களுக்கு அருகிலுள்ள உணவை கண்டறியுங்கள்.",
        "available_near": "உங்களுக்கு அருகிலுள்ள உணவு", "view_all": "அனைத்தையும் காண →",
        "meals_helped": "வழங்கிய உணவுகள்", "people_helped": "உதவி பெற்றவர்கள்",
        "food_saved": "சேமிக்கப்பட்ட உணவு", "active_donors": "செயலில் உள்ள நன்கொடையாளர்கள்",
        "first_time_donor": "முதல் முறை நன்கொடையாளர்", "donor_login": "நன்கொடையாளர் உள்நுழைவு",
        "first_time_receiver": "முதல் முறை பெறுநர்", "receiver_login": "பெறுநர் உள்நுழைவு",
        "create_account": "கணக்கை உருவாக்கு", "login": "உள்நுழைவு", "username": "பயனர் பெயர்",
        "email": "மின்னஞ்சல்", "phone": "தொலைபேசி எண்", "trust_code": "டிரஸ்ட் குறியீடு",
        "welcome_back": "மீண்டும் வரவேற்கிறோம்! தொடர உள்நுழையவும்.",
        "first_registration": "இந்த விவரங்கள் முதல் பதிவு நேரத்தில் மட்டும் கேட்கப்படும்.",
        "food_photo": "உணவு படம்", "food_name": "உணவு பெயர்", "food_category": "உணவு வகை",
        "servings": "பரிமாறல்கள்", "prepared_time": "தயாரித்த நேரம்", "expiry_date": "காலாவதி தேதி",
        "pickup_location": "பெறும் இடம்", "notes": "கூடுதல் குறிப்புகள்", "publish": "நன்கொடையை வெளியிடு",
        "food_description": "உங்களிடம் உள்ள உணவை விவரிக்கவும்", "analyze_find": "ஆய்வு செய்து பெறுநர்களை தேடு",
        "nlp_analysis": "NLP ஆய்வு", "food_type": "உணவு வகை", "quantity": "அளவு",
        "urgency": "அவசரம்", "suitable": "பொருத்தமான பெறுநர்கள்", "receiver_found": "பெறுநர்கள் கண்டறியப்பட்டனர்",
        "no_receiver": "பொருத்தமான பெறுநர் கிடைக்கவில்லை.", "find_food_title": "உணவை தேடுங்கள்",
        "find_food_sub": "உங்களுக்கு அருகிலுள்ள நல்ல உணவை கண்டறியுங்கள்.", "search": "உணவு, இடம் அல்லது நன்கொடையாளரை தேடுங்கள்...",
        "within": "5 கி.மீ.க்குள்", "all_categories": "அனைத்து வகைகள்", "vegetarian": "சைவம்",
        "available_now": "இப்போது கிடைக்கும்", "request": "கோரிக்கை", "accept": "நன்கொடையை ஏற்கவும்",
        "donated_by": "வழங்கியவர்", "verified": "சரிபார்க்கப்பட்ட நன்கொடையாளர்", "distance": "கி.மீ.",
        "language_title": "மொழியை தேர்வு செய்யவும்", "language_sub": "தொடர உங்களுக்கு விருப்பமான மொழியை தேர்வு செய்யவும்.",
        "save_language": "மொழியை சேமி", "notification_title": "அறிவிப்புகள்",
        "notification_sub": "உங்கள் உணவு பயணத்தைப் பற்றிய தகவல்களைப் பெறுங்கள்.", "new_request": "புதிய உணவு கோரிக்கை",
        "request_accepted": "கோரிக்கை ஏற்கப்பட்டது", "pickup_reminder": "பெறும் இட நினைவூட்டல்",
        "donation_completed": "நன்கொடை முடிந்தது", "new_message": "புதிய செய்தி", "profile_title": "என் சுயவிவரம்",
        "good_food": "நல்ல உணவு. சிறந்த தாக்கம்.", "trusted_donor": "நம்பகமான நன்கொடையாளர்",
        "donations": "நன்கொடைகள்", "kg_saved": "சேமித்த உணவு", "edit_profile": "சுயவிவரத்தை திருத்து",
        "privacy": "தனியுரிமை & பாதுகாப்பு", "history_title": "என் உணவு செயல்பாடு", "donation_tab": "நன்கொடைகள்",
        "request_tab": "கோரிக்கைகள்", "no_history": "வரலாறு இல்லை.", "no_notifications": "அறிவிப்புகள் இல்லை.",
        "please_login": "முதலில் உள்நுழையவும்.", "account_created": "கணக்கு வெற்றிகரமாக உருவாக்கப்பட்டது!",
        "login_success": "உள்நுழைவு வெற்றிகரமாக முடிந்தது!", "donation_added": "உணவு நன்கொடை சேர்க்கப்பட்டது!",
        "donation_accepted": "நன்கொடை ஏற்கப்பட்டது!", "donor_notified": "நன்கொடையாளருக்கு அறிவிக்கப்பட்டது.",
        "enter_name": "உங்கள் பயனர் பெயரை உள்ளிடவும்.", "valid_email": "சரியான மின்னஞ்சலை உள்ளிடவும்.",
        "valid_phone": "10 இலக்க தொலைபேசி எண்ணை உள்ளிடவும்.", "enter_trust": "டிரஸ்ட் குறியீட்டை உள்ளிடவும்.",
        "trust_used": "இந்த டிரஸ்ட் குறியீடு ஏற்கனவே பயன்படுத்தப்பட்டுள்ளது.", "name_not_found": "பயனர் பெயர் கிடைக்கவில்லை.",
        "wrong_receiver": "பயனர் பெயர் அல்லது டிரஸ்ட் குறியீடு தவறானது.", "describe_food": "உணவை விவரிக்கவும்.",
        "enter_location": "பெறும் இடத்தை உள்ளிடவும்.", "no_food": "தற்போது உணவு நன்கொடைகள் இல்லை.",
        "meals": "உணவுகள்", "available": "கிடைக்கும்", "accepted": "ஏற்கப்பட்டது", "requested": "கோரப்பட்டது",
        "completed": "முடிந்தது", "normal": "சாதாரணம்",
    },
    "Telugu": {
        "food_donor": "ఫుడ్ డోనర్", "tagline": "మంచి ఆహారం • సంతోషకరమైన జీవితం",
        "together": "కలిసి ఆకలిని అంతం చేద్దాం.", "home": "హోమ్", "donor": "ఆహారం ఇవ్వండి",
        "receiver": "ఆహారం పొందండి", "language": "భాష", "notifications": "నోటిఫికేషన్లు",
        "profile": "నా ప్రొఫైల్", "history": "చరిత్ర", "settings": "సెట్టింగ్స్", "logout": "లాగ్ అవుట్",
        "dashboard": "డాష్‌బోర్డ్", "welcome": "మంచి ఆహారం మంచి రేపటిని సృష్టిస్తుంది.",
        "welcome_name": "హలో, {name} 👋", "share_food": "ఆహారం పంచండి", "support_communities": "సమాజాలకు సహాయం చేయండి",
        "better_tomorrow": "మంచి రేపటిని నిర్మించండి", "donate_card": "ఆహారం దానం చేయండి",
        "donate_card_text": "మీ అదనపు ఆహారాన్ని పంచి మార్పును తీసుకురండి.", "find_card": "ఆహారం కనుగొనండి",
        "find_card_text": "మీ దగ్గరలో అందుబాటులో ఉన్న ఆహారాన్ని కనుగొనండి.", "available_near": "మీ దగ్గరలో అందుబాటులో ఉంది",
        "view_all": "అన్నీ చూడండి →", "meals_helped": "దానం చేసిన భోజనాలు", "people_helped": "సహాయం పొందిన వారు",
        "food_saved": "సేవ్ చేసిన ఆహారం", "active_donors": "యాక్టివ్ డోనర్లు", "first_time_donor": "మొదటిసారి దాత",
        "donor_login": "దాత లాగిన్", "first_time_receiver": "మొదటిసారి స్వీకర్త", "receiver_login": "స్వీకర్త లాగిన్",
        "create_account": "ఖాతా సృష్టించండి", "login": "లాగిన్", "username": "వినియోగదారు పేరు",
        "email": "ఇమెయిల్", "phone": "ఫోన్ నంబర్", "trust_code": "ట్రస్ట్ కోడ్",
        "welcome_back": "మళ్లీ స్వాగతం! కొనసాగడానికి లాగిన్ చేయండి.",
        "first_registration": "ఈ వివరాలు మొదటి రిజిస్ట్రేషన్ సమయంలో మాత్రమే అడుగుతాము.",
        "food_photo": "ఆహారం ఫోటో", "food_name": "ఆహారం పేరు", "food_category": "ఆహార రకం",
        "servings": "సర్వింగ్స్", "prepared_time": "తయారు చేసిన సమయం", "expiry_date": "గడువు తేదీ",
        "pickup_location": "పికప్ స్థలం", "notes": "అదనపు గమనికలు", "publish": "దానాన్ని ప్రచురించండి",
        "food_description": "మీ వద్ద ఉన్న ఆహారాన్ని వివరించండి", "analyze_find": "విశ్లేషించి స్వీకర్తలను కనుగొనండి",
        "nlp_analysis": "NLP విశ్లేషణ", "food_type": "ఆహార రకం", "quantity": "పరిమాణం", "urgency": "అత్యవసరం",
        "suitable": "సరైన స్వీకర్తలు", "receiver_found": "స్వీకర్తలు కనుగొనబడ్డారు", "no_receiver": "సరైన స్వీకర్త కనుగొనబడలేదు.",
        "find_food_title": "ఆహారం కనుగొనండి", "find_food_sub": "మీ దగ్గర మంచి ఆహారాన్ని కనుగొనండి.",
        "search": "ఆహారం, స్థలం లేదా దాతను వెతకండి...", "within": "5 కి.మీ లోపు", "all_categories": "అన్ని రకాలు",
        "vegetarian": "శాకాహారం", "available_now": "ఇప్పుడు అందుబాటులో ఉంది", "request": "అభ్యర్థించండి",
        "accept": "దానాన్ని స్వీకరించండి", "donated_by": "దానం చేసినవారు", "verified": "ధృవీకరించిన దాత", "distance": "కి.మీ",
        "language_title": "భాషను ఎంచుకోండి", "language_sub": "కొనసాగడానికి మీకు ఇష్టమైన భాషను ఎంచుకోండి.",
        "save_language": "భాషను సేవ్ చేయండి", "notification_title": "నోటిఫికేషన్లు",
        "notification_sub": "మీ ఆహార ప్రయాణం గురించి తెలుసుకోండి.", "new_request": "కొత్త ఆహార అభ్యర్థన",
        "request_accepted": "అభ్యర్థన అంగీకరించబడింది", "pickup_reminder": "పికప్ రిమైండర్",
        "donation_completed": "దానం పూర్తయింది", "new_message": "కొత్త సందేశం", "profile_title": "నా ప్రొఫైల్",
        "good_food": "మంచి ఆహారం. గొప్ప ప్రభావం.", "trusted_donor": "నమ్మకమైన దాత", "donations": "దానాలు",
        "people_helped": "సహాయం పొందిన వారు", "kg_saved": "సేవ్ చేసిన ఆహారం", "edit_profile": "ప్రొఫైల్ మార్చండి",
        "privacy": "గోప్యత & భద్రత", "history_title": "నా ఆహార కార్యకలాపాలు", "donation_tab": "దానాలు",
        "request_tab": "అభ్యర్థనలు", "no_history": "చరిత్ర లేదు.", "no_notifications": "నోటిఫికేషన్లు లేవు.",
        "please_login": "ముందుగా లాగిన్ చేయండి.", "account_created": "ఖాతా విజయవంతంగా సృష్టించబడింది!",
        "login_success": "లాగిన్ విజయవంతమైంది!", "donation_added": "ఆహార దానం జోడించబడింది!",
        "donation_accepted": "దానం అంగీకరించబడింది!", "donor_notified": "దాతకు తెలియజేయబడింది.",
        "enter_name": "మీ వినియోగదారు పేరును నమోదు చేయండి.", "valid_email": "చెల్లుబాటు అయ్యే ఇమెయిల్ నమోదు చేయండి.",
        "valid_phone": "10 అంకెల ఫోన్ నంబర్ నమోదు చేయండి.", "enter_trust": "మీ ట్రస్ట్ కోడ్ నమోదు చేయండి.",
        "trust_used": "ఈ ట్రస్ట్ కోడ్ ఇప్పటికే ఉపయోగించబడింది.", "name_not_found": "వినియోగదారు పేరు కనుగొనబడలేదు.",
        "wrong_receiver": "వినియోగదారు పేరు లేదా ట్రస్ట్ కోడ్ తప్పుగా ఉంది.", "describe_food": "ఆహారాన్ని వివరించండి.",
        "enter_location": "పికప్ స్థలాన్ని నమోదు చేయండి.", "no_food": "ప్రస్తుతం ఆహార దానాలు లేవు.",
        "meals": "భోజనాలు", "available": "అందుబాటులో ఉంది", "accepted": "అంగీకరించబడింది",
        "requested": "అభ్యర్థించబడింది", "completed": "పూర్తయింది", "normal": "సాధారణం",
    },
    "Kannada": {
        "food_donor": "ಫುಡ್ ಡೋನರ್", "tagline": "ಉತ್ತಮ ಆಹಾರ • ಸಂತೋಷದ ಜೀವನ",
        "together": "ಒಟ್ಟಾಗಿ ಹಸಿವನ್ನು ಕೊನೆಗೊಳಿಸೋಣ.", "home": "ಮುಖಪುಟ", "donor": "ಆಹಾರ ನೀಡಿ",
        "receiver": "ಆಹಾರ ಹುಡುಕಿ", "language": "ಭಾಷೆ", "notifications": "ಅಧಿಸೂಚನೆಗಳು", "profile": "ನನ್ನ ಪ್ರೊಫೈಲ್",
        "history": "ಇತಿಹಾಸ", "settings": "ಸೆಟ್ಟಿಂಗ್ಸ್", "logout": "ಲಾಗ್ ಔಟ್", "dashboard": "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        "welcome": "ಉತ್ತಮ ಆಹಾರವು ಉತ್ತಮ ನಾಳೆಯನ್ನು ನಿರ್ಮಿಸುತ್ತದೆ.", "welcome_name": "ಹಲೋ, {name} 👋",
        "share_food": "ಆಹಾರ ಹಂಚಿಕೊಳ್ಳಿ", "support_communities": "ಸಮುದಾಯಗಳಿಗೆ ಸಹಾಯ ಮಾಡಿ",
        "better_tomorrow": "ಉತ್ತಮ ನಾಳೆಯನ್ನು ನಿರ್ಮಿಸಿ", "donate_card": "ಆಹಾರ ದಾನ ಮಾಡಿ",
        "donate_card_text": "ನಿಮ್ಮ ಹೆಚ್ಚುವರಿ ಆಹಾರವನ್ನು ಹಂಚಿಕೊಂಡು ಬದಲಾವಣೆ ತರಿರಿ.", "find_card": "ಆಹಾರ ಹುಡುಕಿ",
        "find_card_text": "ನಿಮ್ಮ ಹತ್ತಿರ ಲಭ್ಯವಿರುವ ಆಹಾರವನ್ನು ಕಂಡುಹಿಡಿಯಿರಿ.", "available_near": "ನಿಮ್ಮ ಹತ್ತಿರ ಲಭ್ಯವಿದೆ",
        "view_all": "ಎಲ್ಲವನ್ನೂ ನೋಡಿ →", "meals_helped": "ದಾನ ಮಾಡಿದ ಊಟಗಳು", "people_helped": "ಸಹಾಯ ಪಡೆದವರು",
        "food_saved": "ಉಳಿಸಿದ ಆಹಾರ", "active_donors": "ಸಕ್ರಿಯ ದಾನಿಗಳು", "first_time_donor": "ಮೊದಲ ಬಾರಿಗೆ ದಾನಿ",
        "donor_login": "ದಾನಿ ಲಾಗಿನ್", "first_time_receiver": "ಮೊದಲ ಬಾರಿಗೆ ಸ್ವೀಕರಿಸುವವರು",
        "receiver_login": "ಸ್ವೀಕರಿಸುವವರ ಲಾಗಿನ್", "create_account": "ಖಾತೆ ರಚಿಸಿ", "login": "ಲಾಗಿನ್",
        "username": "ಬಳಕೆದಾರ ಹೆಸರು", "email": "ಇಮೇಲ್", "phone": "ದೂರವಾಣಿ ಸಂಖ್ಯೆ", "trust_code": "ಟ್ರಸ್ಟ್ ಕೋಡ್",
        "welcome_back": "ಮತ್ತೆ ಸ್ವಾಗತ! ಮುಂದುವರಿಯಲು ಲಾಗಿನ್ ಮಾಡಿ.", "first_registration": "ಈ ವಿವರಗಳನ್ನು ಮೊದಲ ನೋಂದಣಿಯಲ್ಲಿ ಮಾತ್ರ ಕೇಳಲಾಗುತ್ತದೆ.",
        "food_photo": "ಆಹಾರದ ಚಿತ್ರ", "food_name": "ಆಹಾರದ ಹೆಸರು", "food_category": "ಆಹಾರದ ಪ್ರಕಾರ",
        "servings": "ಸರ್ವಿಂಗ್ಸ್", "prepared_time": "ತಯಾರಿಸಿದ ಸಮಯ", "expiry_date": "ಅವಧಿ ಮುಗಿಯುವ ದಿನಾಂಕ",
        "pickup_location": "ಪಿಕಪ್ ಸ್ಥಳ", "notes": "ಹೆಚ್ಚುವರಿ ಟಿಪ್ಪಣಿಗಳು", "publish": "ದಾನ ಪ್ರಕಟಿಸಿ",
        "food_description": "ನಿಮ್ಮಲ್ಲಿರುವ ಆಹಾರವನ್ನು ವಿವರಿಸಿ", "analyze_find": "ವಿಶ್ಲೇಷಿಸಿ ಸ್ವೀಕರಿಸುವವರನ್ನು ಹುಡುಕಿ",
        "nlp_analysis": "NLP ವಿಶ್ಲೇಷಣೆ", "food_type": "ಆಹಾರದ ಪ್ರಕಾರ", "quantity": "ಪ್ರಮಾಣ", "urgency": "ತುರ್ತು",
        "suitable": "ಸೂಕ್ತ ಸ್ವೀಕರಿಸುವವರು", "receiver_found": "ಸ್ವೀಕರಿಸುವವರು ಕಂಡುಬಂದಿದ್ದಾರೆ",
        "no_receiver": "ಸೂಕ್ತ ಸ್ವೀಕರಿಸುವವರು ಕಂಡುಬಂದಿಲ್ಲ.", "find_food_title": "ಆಹಾರ ಹುಡುಕಿ",
        "find_food_sub": "ನಿಮ್ಮ ಹತ್ತಿರ ಉತ್ತಮ ಆಹಾರವನ್ನು ಹುಡುಕಿ.", "search": "ಆಹಾರ, ಸ್ಥಳ ಅಥವಾ ದಾನಿಯನ್ನು ಹುಡುಕಿ...",
        "within": "5 ಕಿ.ಮೀ ಒಳಗೆ", "all_categories": "ಎಲ್ಲಾ ವರ್ಗಗಳು", "vegetarian": "ಸಸ್ಯಾಹಾರಿ",
        "available_now": "ಈಗ ಲಭ್ಯವಿದೆ", "request": "ವಿನಂತಿಸಿ", "accept": "ದಾನ ಸ್ವೀಕರಿಸಿ",
        "donated_by": "ದಾನ ಮಾಡಿದವರು", "verified": "ಪರಿಶೀಲಿಸಿದ ದಾನಿ", "distance": "ಕಿ.ಮೀ",
        "language_title": "ಭಾಷೆ ಆಯ್ಕೆಮಾಡಿ", "language_sub": "ಮುಂದುವರಿಯಲು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.",
        "save_language": "ಭಾಷೆ ಉಳಿಸಿ", "notification_title": "ಅಧಿಸೂಚನೆಗಳು",
        "notification_sub": "ನಿಮ್ಮ ಆಹಾರ ಪ್ರಯಾಣದ ಬಗ್ಗೆ ಮಾಹಿತಿ ಪಡೆಯಿರಿ.", "new_request": "ಹೊಸ ಆಹಾರ ವಿನಂತಿ",
        "request_accepted": "ವಿನಂತಿ ಸ್ವೀಕರಿಸಲಾಗಿದೆ", "pickup_reminder": "ಪಿಕಪ್ ನೆನಪಿನ ಸೂಚನೆ",
        "donation_completed": "ದಾನ ಪೂರ್ಣಗೊಂಡಿದೆ", "new_message": "ಹೊಸ ಸಂದೇಶ", "profile_title": "ನನ್ನ ಪ್ರೊಫೈಲ್",
        "good_food": "ಉತ್ತಮ ಆಹಾರ. ಉತ್ತಮ ಪರಿಣಾಮ.", "trusted_donor": "ವಿಶ್ವಾಸಾರ್ಹ ದಾನಿ", "donations": "ದಾನಗಳು",
        "kg_saved": "ಉಳಿಸಿದ ಆಹಾರ", "edit_profile": "ಪ್ರೊಫೈಲ್ ಸಂಪಾದಿಸಿ", "privacy": "ಗೌಪ್ಯತೆ & ಭದ್ರತೆ",
        "history_title": "ನನ್ನ ಆಹಾರ ಚಟುವಟಿಕೆ", "donation_tab": "ದಾನಗಳು", "request_tab": "ವಿನಂತಿಗಳು",
        "no_history": "ಇತಿಹಾಸವಿಲ್ಲ.", "no_notifications": "ಯಾವುದೇ ಅಧಿಸೂಚನೆಗಳಿಲ್ಲ.", "please_login": "ಮೊದಲು ಲಾಗಿನ್ ಮಾಡಿ.",
        "account_created": "ಖಾತೆ ಯಶಸ್ವಿಯಾಗಿ ರಚಿಸಲಾಗಿದೆ!", "login_success": "ಲಾಗಿನ್ ಯಶಸ್ವಿಯಾಗಿದೆ!",
        "donation_added": "ಆಹಾರ ದಾನ ಸೇರಿಸಲಾಗಿದೆ!", "donation_accepted": "ದಾನ ಸ್ವೀಕರಿಸಲಾಗಿದೆ!",
        "donor_notified": "ದಾನಿಗೆ ತಿಳಿಸಲಾಗಿದೆ.", "enter_name": "ನಿಮ್ಮ ಬಳಕೆದಾರ ಹೆಸರನ್ನು ನಮೂದಿಸಿ.",
        "valid_email": "ಸರಿಯಾದ ಇಮೇಲ್ ನಮೂದಿಸಿ.", "valid_phone": "10 ಅಂಕಿಯ ದೂರವಾಣಿ ಸಂಖ್ಯೆ ನಮೂದಿಸಿ.",
        "enter_trust": "ಟ್ರಸ್ಟ್ ಕೋಡ್ ನಮೂದಿಸಿ.", "trust_used": "ಈ ಟ್ರಸ್ಟ್ ಕೋಡ್ ಈಗಾಗಲೇ ಬಳಸಲಾಗಿದೆ.",
        "name_not_found": "ಬಳಕೆದಾರ ಹೆಸರು ಕಂಡುಬಂದಿಲ್ಲ.", "wrong_receiver": "ಬಳಕೆದಾರ ಹೆಸರು ಅಥವಾ ಟ್ರಸ್ಟ್ ಕೋಡ್ ತಪ್ಪಾಗಿದೆ.",
        "describe_food": "ಆಹಾರವನ್ನು ವಿವರಿಸಿ.", "enter_location": "ಪಿಕಪ್ ಸ್ಥಳವನ್ನು ನಮೂದಿಸಿ.",
        "no_food": "ಪ್ರಸ್ತುತ ಯಾವುದೇ ಆಹಾರ ದಾನಗಳು ಇಲ್ಲ.", "meals": "ಊಟಗಳು", "available": "ಲಭ್ಯವಿದೆ",
        "accepted": "ಸ್ವೀಕರಿಸಲಾಗಿದೆ", "requested": "ವಿನಂತಿಸಲಾಗಿದೆ", "completed": "ಪೂರ್ಣಗೊಂಡಿದೆ", "normal": "ಸಾಮಾನ್ಯ",
    },
    "Hindi": {
        "food_donor": "फूड डोनर", "tagline": "अच्छा भोजन • खुशहाल जीवन", "together": "मिलकर भूख को खत्म करें.",
        "home": "होम", "donor": "भोजन दें", "receiver": "भोजन खोजें", "language": "भाषा", "notifications": "सूचनाएं",
        "profile": "मेरी प्रोफ़ाइल", "history": "इतिहास", "settings": "सेटिंग्स", "logout": "लॉग आउट",
        "dashboard": "डैशबोर्ड", "welcome": "अच्छा भोजन बेहतर कल बनाता है.", "welcome_name": "नमस्ते, {name} 👋",
        "share_food": "भोजन साझा करें", "support_communities": "समुदायों की मदद करें", "better_tomorrow": "बेहतर कल बनाएं",
        "donate_card": "भोजन दान करें", "donate_card_text": "अपना अतिरिक्त भोजन साझा करके बदलाव लाएं.",
        "find_card": "भोजन खोजें", "find_card_text": "अपने पास उपलब्ध भोजन खोजें.", "available_near": "आपके पास उपलब्ध",
        "view_all": "सभी देखें →", "meals_helped": "दान किए गए भोजन", "people_helped": "लाभार्थी",
        "food_saved": "बचाया गया भोजन", "active_donors": "सक्रिय दाता", "first_time_donor": "पहली बार दाता",
        "donor_login": "दाता लॉगिन", "first_time_receiver": "पहली बार प्राप्तकर्ता", "receiver_login": "प्राप्तकर्ता लॉगिन",
        "create_account": "खाता बनाएं", "login": "लॉगिन", "username": "उपयोगकर्ता नाम", "email": "ईमेल",
        "phone": "फोन नंबर", "trust_code": "ट्रस्ट कोड", "welcome_back": "वापसी पर स्वागत है! जारी रखने के लिए लॉगिन करें.",
        "first_registration": "ये विवरण केवल पहली बार पंजीकरण के समय पूछे जाएंगे.", "food_photo": "भोजन फोटो",
        "food_name": "भोजन का नाम", "food_category": "भोजन श्रेणी", "servings": "सर्विंग्स", "prepared_time": "तैयार समय",
        "expiry_date": "समाप्ति तिथि", "pickup_location": "पिकअप स्थान", "notes": "अतिरिक्त नोट्स",
        "publish": "दान प्रकाशित करें", "food_description": "उपलब्ध भोजन का विवरण दें",
        "analyze_find": "विश्लेषण करें और प्राप्तकर्ता खोजें", "nlp_analysis": "NLP विश्लेषण", "food_type": "भोजन प्रकार",
        "quantity": "मात्रा", "urgency": "तत्कालता", "suitable": "उपयुक्त प्राप्तकर्ता", "receiver_found": "प्राप्तकर्ता मिले",
        "no_receiver": "कोई उपयुक्त प्राप्तकर्ता नहीं मिला.", "find_food_title": "भोजन खोजें", "find_food_sub": "अपने पास अच्छा भोजन खोजें.",
        "search": "भोजन, स्थान या दाता खोजें...", "within": "5 किमी के अंदर", "all_categories": "सभी श्रेणियां",
        "vegetarian": "शाकाहारी", "available_now": "अभी उपलब्ध", "request": "अनुरोध", "accept": "दान स्वीकार करें",
        "donated_by": "दानकर्ता", "verified": "सत्यापित दाता", "distance": "किमी", "language_title": "भाषा चुनें",
        "language_sub": "जारी रखने के लिए अपनी पसंदीदा भाषा चुनें.", "save_language": "भाषा सहेजें",
        "notification_title": "सूचनाएं", "notification_sub": "अपनी भोजन यात्रा से अपडेट रहें.", "new_request": "नई भोजन अनुरोध",
        "request_accepted": "अनुरोध स्वीकार किया गया", "pickup_reminder": "पिकअप रिमाइंडर",
        "donation_completed": "दान पूरा हुआ", "new_message": "नया संदेश", "profile_title": "मेरी प्रोफ़ाइल",
        "good_food": "अच्छा भोजन. बड़ा प्रभाव.", "trusted_donor": "विश्वसनीय दाता", "donations": "दान",
        "kg_saved": "बचाया गया भोजन", "edit_profile": "प्रोफ़ाइल संपादित करें", "privacy": "गोपनीयता और सुरक्षा",
        "history_title": "मेरी भोजन गतिविधि", "donation_tab": "दान", "request_tab": "अनुरोध",
        "no_history": "कोई इतिहास नहीं.", "no_notifications": "अभी कोई सूचना नहीं.", "please_login": "पहले लॉगिन करें.",
        "account_created": "खाता सफलतापूर्वक बनाया गया!", "login_success": "लॉगिन सफल हुआ!",
        "donation_added": "भोजन दान जोड़ा गया!", "donation_accepted": "दान स्वीकार किया गया!",
        "donor_notified": "दाता को सूचित किया गया.", "enter_name": "अपना उपयोगकर्ता नाम दर्ज करें.",
        "valid_email": "मान्य ईमेल दर्ज करें.", "valid_phone": "10 अंकों का फोन नंबर दर्ज करें.",
        "enter_trust": "ट्रस्ट कोड दर्ज करें.", "trust_used": "यह ट्रस्ट कोड पहले से उपयोग में है.",
        "name_not_found": "उपयोगकर्ता नाम नहीं मिला.", "wrong_receiver": "उपयोगकर्ता नाम या ट्रस्ट कोड गलत है.",
        "describe_food": "भोजन का विवरण दें.", "enter_location": "पिकअप स्थान दर्ज करें.",
        "no_food": "अभी कोई भोजन दान उपलब्ध नहीं है.", "meals": "भोजन", "available": "उपलब्ध",
        "accepted": "स्वीकृत", "requested": "अनुरोधित", "completed": "पूर्ण", "normal": "सामान्य",
    },
    "Malayalam": {
        "food_donor": "ഫുഡ് ഡോണർ", "tagline": "നല്ല ഭക്ഷണം • സന്തോഷകരമായ ജീവിതം", "together": "ഒരുമിച്ച് വിശപ്പ് അവസാനിപ്പിക്കാം.",
        "home": "ഹോം", "donor": "ഭക്ഷണം നൽകുക", "receiver": "ഭക്ഷണം കണ്ടെത്തുക", "language": "ഭാഷ",
        "notifications": "അറിയിപ്പുകൾ", "profile": "എന്റെ പ്രൊഫൈൽ", "history": "ചരിത്രം", "settings": "ക്രമീകരണങ്ങൾ",
        "logout": "ലോഗ് ഔട്ട്", "dashboard": "ഡാഷ്ബോർഡ്", "welcome": "നല്ല ഭക്ഷണം മികച്ച നാളെ സൃഷ്ടിക്കുന്നു.",
        "welcome_name": "ഹലോ, {name} 👋", "share_food": "ഭക്ഷണം പങ്കിടുക", "support_communities": "സമൂഹങ്ങളെ സഹായിക്കുക",
        "better_tomorrow": "മികച്ച നാളെ നിർമ്മിക്കുക", "donate_card": "ഭക്ഷണം നൽകുക",
        "donate_card_text": "അധികമുള്ള ഭക്ഷണം പങ്കിട്ട് മാറ്റം സൃഷ്ടിക്കുക.", "find_card": "ഭക്ഷണം കണ്ടെത്തുക",
        "find_card_text": "നിങ്ങളുടെ അടുത്തുള്ള ലഭ്യമായ ഭക്ഷണം കണ്ടെത്തുക.", "available_near": "നിങ്ങളുടെ അടുത്ത് ലഭ്യം",
        "view_all": "എല്ലാം കാണുക →", "meals_helped": "നൽകിയ ഭക്ഷണങ്ങൾ", "people_helped": "സഹായം ലഭിച്ചവർ",
        "food_saved": "സംരക്ഷിച്ച ഭക്ഷണം", "active_donors": "സജീവ ഡോണർമാർ", "first_time_donor": "ആദ്യമായി ഡോണർ",
        "donor_login": "ഡോണർ ലോഗിൻ", "first_time_receiver": "ആദ്യമായി സ്വീകരിക്കുന്നവർ", "receiver_login": "സ്വീകർത്താവ് ലോഗിൻ",
        "create_account": "അക്കൗണ്ട് സൃഷ്ടിക്കുക", "login": "ലോഗിൻ", "username": "ഉപയോക്തൃ പേര്", "email": "ഇമെയിൽ",
        "phone": "ഫോൺ നമ്പർ", "trust_code": "ട്രസ്റ്റ് കോഡ്", "welcome_back": "വീണ്ടും സ്വാഗതം! തുടരാൻ ലോഗിൻ ചെയ്യുക.",
        "first_registration": "ഈ വിവരങ്ങൾ ആദ്യ രജിസ്ട്രേഷനിൽ മാത്രം ചോദിക്കും.", "food_photo": "ഭക്ഷണ ചിത്രം",
        "food_name": "ഭക്ഷണ പേര്", "food_category": "ഭക്ഷണ വിഭാഗം", "servings": "സെർവിംഗ്സ്", "prepared_time": "തയ്യാറാക്കിയ സമയം",
        "expiry_date": "കാലാവധി തീയതി", "pickup_location": "പിക്കപ്പ് സ്ഥലം", "notes": "അധിക കുറിപ്പുകൾ",
        "publish": "ഡൊണേഷൻ പ്രസിദ്ധീകരിക്കുക", "food_description": "ലഭ്യമായ ഭക്ഷണം വിവരിക്കുക",
        "analyze_find": "വിശകലനം ചെയ്ത് സ്വീകർത്താക്കളെ കണ്ടെത്തുക", "nlp_analysis": "NLP വിശകലനം",
        "food_type": "ഭക്ഷണ തരം", "quantity": "അളവ്", "urgency": "അടിയന്തരത", "suitable": "അനുയോജ്യ സ്വീകർത്താക്കൾ",
        "receiver_found": "സ്വീകർത്താക്കളെ കണ്ടെത്തി", "no_receiver": "അനുയോജ്യമായ സ്വീകർത്താവിനെ കണ്ടെത്താനായില്ല.",
        "find_food_title": "ഭക്ഷണം കണ്ടെത്തുക", "find_food_sub": "നിങ്ങളുടെ അടുത്തുള്ള നല്ല ഭക്ഷണം കണ്ടെത്തുക.",
        "search": "ഭക്ഷണം, സ്ഥലം അല്ലെങ്കിൽ ഡോണറെ തിരയുക...", "within": "5 കി.മീ ഉള്ളിൽ", "all_categories": "എല്ലാ വിഭാഗങ്ങളും",
        "vegetarian": "വെജിറ്റേറിയൻ", "available_now": "ഇപ്പോൾ ലഭ്യം", "request": "അഭ്യർത്ഥിക്കുക",
        "accept": "ഡൊണേഷൻ സ്വീകരിക്കുക", "donated_by": "നൽകിയത്", "verified": "സ്ഥിരീകരിച്ച ഡോണർ", "distance": "കി.മീ",
        "language_title": "ഭാഷ തിരഞ്ഞെടുക്കുക", "language_sub": "തുടരാൻ ഇഷ്ടമുള്ള ഭാഷ തിരഞ്ഞെടുക്കുക.",
        "save_language": "ഭാഷ സംരക്ഷിക്കുക", "notification_title": "അറിയിപ്പുകൾ",
        "notification_sub": "നിങ്ങളുടെ ഭക്ഷണ യാത്രയുടെ അപ്ഡേറ്റുകൾ നേടുക.", "new_request": "പുതിയ ഭക്ഷണ അഭ്യർത്ഥന",
        "request_accepted": "അഭ്യർത്ഥന സ്വീകരിച്ചു", "pickup_reminder": "പിക്കപ്പ് ഓർമ്മപ്പെടുത്തൽ",
        "donation_completed": "ഡൊണേഷൻ പൂർത്തിയായി", "new_message": "പുതിയ സന്ദേശം", "profile_title": "എന്റെ പ്രൊഫൈൽ",
        "good_food": "നല്ല ഭക്ഷണം. മികച്ച സ്വാധീനം.", "trusted_donor": "വിശ്വസനീയ ഡോണർ", "donations": "ഡൊണേഷനുകൾ",
        "kg_saved": "സംരക്ഷിച്ച ഭക്ഷണം", "edit_profile": "പ്രൊഫൈൽ തിരുത്തുക", "privacy": "സ്വകാര്യത & സുരക്ഷ",
        "history_title": "എന്റെ ഭക്ഷണ പ്രവർത്തനം", "donation_tab": "ഡൊണേഷനുകൾ", "request_tab": "അഭ്യർത്ഥനകൾ",
        "no_history": "ചരിത്രമില്ല.", "no_notifications": "അറിയിപ്പുകളൊന്നുമില്ല.", "please_login": "ആദ്യം ലോഗിൻ ചെയ്യുക.",
        "account_created": "അക്കൗണ്ട് വിജയകരമായി സൃഷ്ടിച്ചു!", "login_success": "ലോഗിൻ വിജയകരമായി!",
        "donation_added": "ഭക്ഷണ ഡൊണേഷൻ ചേർത്തു!", "donation_accepted": "ഡൊണേഷൻ സ്വീകരിച്ചു!",
        "donor_notified": "ഡോണറെ അറിയിച്ചു.", "enter_name": "ഉപയോക്തൃ പേര് നൽകുക.",
        "valid_email": "ശരിയായ ഇമെയിൽ നൽകുക.", "valid_phone": "10 അക്ക ഫോൺ നമ്പർ നൽകുക.",
        "enter_trust": "ട്രസ്റ്റ് കോഡ് നൽകുക.", "trust_used": "ഈ ട്രസ്റ്റ് കോഡ് ഇതിനകം ഉപയോഗിച്ചു.",
        "name_not_found": "ഉപയോക്തൃ പേര് കണ്ടെത്തിയില്ല.", "wrong_receiver": "പേര് അല്ലെങ്കിൽ ട്രസ്റ്റ് കോഡ് തെറ്റാണ്.",
        "describe_food": "ഭക്ഷണം വിവരിക്കുക.", "enter_location": "പിക്കപ്പ് സ്ഥലം നൽകുക.",
        "no_food": "നിലവിൽ ഭക്ഷണ ഡൊണേഷനുകളില്ല.", "meals": "ഭക്ഷണങ്ങൾ", "available": "ലഭ്യം",
        "accepted": "സ്വീകരിച്ചു", "requested": "അഭ്യർത്ഥിച്ചു", "completed": "പൂർത്തിയായി", "normal": "സാധാരണ",
    },
}


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "app_started": False,
    "logged_in": False,
    "role": "",
    "user_name": "",
    "user_email": "",
    "phone": "",
    "trust_code": "",
    "page": "Home",
    "language": "English",
    "notifications": [],
    "last_matches": [],
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def t(key, **kwargs):
    value = TEXT.get(st.session_state.language, TEXT["English"]).get(
        key, TEXT["English"].get(key, key)
    )
    return value.format(**kwargs) if kwargs else value


# =========================================================
# DATA HELPERS
# =========================================================

def load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_users():
    return load_json(USER_FILE, [])


def save_users(data):
    save_json(USER_FILE, data)


def load_donations():
    return load_json(DONATION_FILE, [])


def save_donations(data):
    save_json(DONATION_FILE, data)


def valid_email(email):
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))


def valid_phone(phone):
    return len(re.sub(r"\D", "", phone)) == 10


def find_donor(name):
    wanted = name.strip().lower()
    for user in load_users():
        if user.get("role") == "Donor" and user.get("name", "").strip().lower() == wanted:
            return user
    return None


def find_receiver(name, trust_code):
    wanted_name = name.strip().lower()
    wanted_code = trust_code.strip().lower()
    for user in load_users():
        if (
            user.get("role") == "Receiver"
            and user.get("name", "").strip().lower() == wanted_name
            and user.get("trust_code", "").strip().lower() == wanted_code
        ):
            return user
    return None


def donor_exists():
    return any(u.get("role") == "Donor" for u in load_users())


def receiver_exists():
    return any(u.get("role") == "Receiver" for u in load_users())


def trust_code_exists(code):
    wanted = code.strip().lower()
    return any(
        u.get("role") == "Receiver"
        and u.get("trust_code", "").strip().lower() == wanted
        for u in load_users()
    )


def login_user(user):
    st.session_state.logged_in = True
    st.session_state.role = user.get("role", "")
    st.session_state.user_name = user.get("name", "")
    st.session_state.user_email = user.get("email", "")
    st.session_state.phone = user.get("phone", "")
    st.session_state.trust_code = user.get("trust_code", "")
    st.session_state.page = "Home"


def logout_user():
    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.phone = ""
    st.session_state.trust_code = ""
    st.session_state.page = "Home"


# =========================================================
# CSS - REFERENCE DESIGN
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@500;600;700&display=swap');

:root {
    --cream: #f7f7ec;
    --cream2: #fffdf5;
    --dark-green: #0d4b37;
    --green: #2f7650;
    --sage: #a9c66b;
    --light-green: #eaf3df;
    --coral: #f26958;
    --coral-light: #ffe2dc;
    --text: #18352a;
    --muted: #6c776f;
    --line: #dfe6d9;
    --white: #ffffff;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 5% 8%, rgba(169,198,107,.18), transparent 18%),
        radial-gradient(circle at 96% 88%, rgba(242,105,88,.10), transparent 20%),
        var(--cream);
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1240px;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: #fbfaf1;
    border-right: 1px solid #e5eadf;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.2rem;
}

section[data-testid="stSidebar"] .stButton button,
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border-radius: 12px;
}

.brand {
    padding: 5px 6px 18px;
}

.brand-title {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    font-weight: 700;
    letter-spacing: .4px;
}

.brand-sub {
    color: var(--green);
    font-size: 12px;
    margin-top: 2px;
}

.page-title {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 0;
}

.page-subtitle {
    color: var(--muted);
    font-size: 14px;
    margin: 3px 0 22px;
}

.hero {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    padding: 27px 34px;
    min-height: 155px;
    background:
        radial-gradient(circle at 88% 15%, rgba(255,255,255,.8), transparent 18%),
        linear-gradient(105deg, #fff7ec, #edf5df);
    border: 1px solid #e4e8dc;
    box-shadow: 0 8px 25px rgba(40,65,50,.07);
}

.hero:after {
    content: "♡";
    position: absolute;
    right: 45px;
    bottom: -30px;
    font-size: 125px;
    color: rgba(242,105,88,.16);
    transform: rotate(-12deg);
}

.hero h2 {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    margin: 0 0 7px;
}

.hero p {
    color: #607067;
    max-width: 530px;
    margin: 0;
    font-size: 14px;
}

.mini-features {
    display: flex;
    gap: 28px;
    margin-top: 18px;
}

.mini-feature {
    font-size: 12px;
    color: var(--dark-green);
    font-weight: 600;
}

.mini-icon {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: #e9f1df;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-right: 7px;
}

.section-title {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 21px;
    font-weight: 700;
    margin: 26px 0 12px;
}

.action-card {
    min-height: 155px;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid var(--line);
    box-shadow: 0 6px 20px rgba(40,65,50,.05);
}

.action-card.coral {
    background: linear-gradient(135deg, #ffe9e2, #fff5ef);
}

.action-card.green {
    background: linear-gradient(135deg, #eaf4df, #f6faef);
}

.action-card h3 {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    margin: 0 0 6px;
    font-size: 20px;
}

.action-card p {
    color: var(--muted);
    font-size: 13px;
    min-height: 38px;
}

.food-card {
    background: #fffef9;
    border: 1px solid #e2e7dc;
    border-radius: 17px;
    padding: 10px;
    box-shadow: 0 5px 17px rgba(42,63,49,.06);
    height: 100%;
}

.food-photo {
    height: 112px;
    border-radius: 13px;
    background: linear-gradient(135deg, #e8e4c9, #f5eee0);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    overflow: hidden;
}

.food-name {
    color: var(--dark-green);
    font-weight: 700;
    margin: 10px 3px 4px;
}

.food-meta {
    color: var(--muted);
    font-size: 11px;
    margin: 2px 3px;
}

.stat-box {
    background: #fffef9;
    border: 1px solid var(--line);
    border-radius: 15px;
    text-align: center;
    padding: 14px 8px;
}

.stat-number {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 25px;
    font-weight: 700;
}

.stat-label {
    color: var(--muted);
    font-size: 10px;
    margin-top: 2px;
}

.form-card {
    background: rgba(255,255,249,.92);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(40,65,50,.06);
}

.login-card {
    max-width: 650px;
    margin: 10px auto;
}

.soft-panel {
    background: #f7faef;
    border: 1px solid #e0e8d6;
    border-radius: 16px;
    padding: 17px;
}

.noti-card {
    background: #fffef9;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 15px 17px;
    margin-bottom: 10px;
}

.profile-card {
    background: #fffef9;
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 26px;
    box-shadow: 0 7px 23px rgba(40,65,50,.05);
}

.avatar {
    width: 92px;
    height: 92px;
    border-radius: 50%;
    background: linear-gradient(135deg, #f5d5c8, #dfe8cc);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 43px;
    margin-bottom: 10px;
}

.profile-name {
    color: var(--dark-green);
    font-family: 'Playfair Display', serif;
    font-size: 27px;
    font-weight: 700;
}

.badge {
    display: inline-block;
    padding: 4px 9px;
    background: #e5f1d8;
    color: #356b48;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 700;
}

.language-box {
    max-width: 650px;
    margin: 0 auto;
    text-align: center;
    background: #fffef9;
    border: 1px solid var(--line);
    border-radius: 22px;
    padding: 35px;
    box-shadow: 0 8px 25px rgba(40,65,50,.06);
}

.language-globe {
    font-size: 50px;
    margin-bottom: 7px;
}

.small-muted {
    color: var(--muted);
    font-size: 12px;
}

div.stButton > button {
    border: 0;
    border-radius: 12px;
    min-height: 42px;
    font-weight: 600;
    background: var(--coral);
    color: white;
    box-shadow: 0 5px 13px rgba(242,105,88,.18);
}

div.stButton > button:hover {
    background: #e95b4b;
    color: white;
    border: 0;
}

.secondary-btn div.stButton > button {
    background: #eaf2df;
    color: var(--dark-green);
    box-shadow: none;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input,
.stDateInput input,
.stTimeInput input,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 11px !important;
    border-color: #d9e2d3 !important;
    background: #fffefb !important;
}

[data-testid="stMetric"] {
    background: #fffef9;
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 10px;
}

hr {
    border-color: #e3e8de;
}

footer {
    visibility: hidden;
}

.leaf-decoration {
    text-align: right;
    color: #8eb35e;
    font-size: 24px;
    letter-spacing: 8px;
    margin-bottom: -8px;
}

@media (max-width: 900px) {
    .page-title { font-size: 30px; }
    .hero { padding: 22px; }
    .mini-features { gap: 10px; flex-wrap: wrap; }
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# FIRST PAGE
# =========================================================

if not st.session_state.app_started:
    image_path = os.path.join(ASSET_DIR, "food_doner_home.png")

    # The supplied landing image remains the full-screen first page.
    if os.path.exists(image_path):
        import base64

        with open(image_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        st.markdown(
            f"""
            <style>
            .block-container {{
                padding: 0 !important;
                max-width: 100% !important;
            }}
            [data-testid="stHeader"], [data-testid="stToolbar"] {{
                display:none !important;
            }}
            .landing {{
                width:100vw;
                height:100vh;
                overflow:hidden;
                position:relative;
                background:#f8f7ec;
            }}
            .landing img {{
                width:100%;
                height:100%;
                object-fit:cover;
                display:block;
            }}
            .landing a {{
                position:absolute;
                inset:0;
                cursor:pointer;
            }}
            </style>
            <div class="landing">
                <img src="data:image/png;base64,{encoded}" alt="Food Donor">
                <a href="?open=1" aria-label="Open Food Donor"></a>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.query_params.get("open") == "1":
            st.session_state.app_started = True
            st.query_params.clear()
            st.rerun()
    else:
        st.markdown(
            """
            <div class="hero" style="min-height:80vh;display:flex;align-items:center;">
                <div>
                    <h2>FOOD DONOR</h2>
                    <p>Good Food • Happy Life</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("OPEN", use_container_width=True):
            st.session_state.app_started = True
            st.rerun()

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand">
            <div class="brand-title">♡ {t("food_donor")}</div>
            <div class="brand-sub">{t("tagline")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    page_options = [
        ("Home", t("home")),
        ("Donor", t("donor")),
        ("Receiver", t("receiver")),
        ("History", t("history")),
        ("Notifications", t("notifications")),
        ("Language", t("language")),
        ("My Profile", t("profile")),
        ("Settings", t("settings")),
    ]

    icons = {
        "Home": "⌂",
        "Donor": "♧",
        "Receiver": "⌕",
        "History": "◷",
        "Notifications": "♢",
        "Language": "◎",
        "My Profile": "♙",
        "Settings": "⚙",
    }

    for page_key, label in page_options:
        active = st.session_state.page == page_key
        if st.button(
            f"{icons[page_key]}   {label}",
            key=f"nav_{page_key}",
            use_container_width=True,
        ):
            st.session_state.page = page_key
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    if st.session_state.logged_in:
        st.markdown(
            f"""
            <div class="small-muted">
                👤 <b>{st.session_state.user_name}</b><br>
                {st.session_state.role}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🚪 " + t("logout"), use_container_width=True):
            logout_user()
            st.rerun()


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":
    if st.session_state.logged_in:
        greeting = t("welcome_name", name=st.session_state.user_name)
    else:
        greeting = t("food_donor")

    st.markdown(
        f"""
        <div class="hero">
            <h2>{greeting}</h2>
            <p>{t("welcome")}</p>
            <div class="mini-features">
                <div class="mini-feature"><span class="mini-icon">🥗</span>{t("share_food")}</div>
                <div class="mini-feature"><span class="mini-icon">♧</span>{t("support_communities")}</div>
                <div class="mini-feature"><span class="mini-icon">♡</span>{t("better_tomorrow")}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(f'<div class="section-title">{t("dashboard")}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div class="action-card coral">
                <h3>🍱 {t("donate_card")}</h3>
                <p>{t("donate_card_text")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("→  " + t("donate_card"), key="home_donate", use_container_width=True):
            st.session_state.page = "Donor"
            st.rerun()

    with c2:
        st.markdown(
            f"""
            <div class="action-card green">
                <h3>🥗 {t("find_card")}</h3>
                <p>{t("find_card_text")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("→  " + t("find_card"), key="home_find", use_container_width=True):
            st.session_state.page = "Receiver"
            st.rerun()

    st.markdown(f'<div class="section-title">{t("available_near")}</div>', unsafe_allow_html=True)

    donations = [d for d in load_donations() if d.get("status", "Available") == "Available"]
    sample = donations[:3]

    if not sample:
        sample = [
            {"food": "Cooked Rice & Vegetables", "quantity": 20, "location": "Chennai", "urgency": "Normal", "donor_name": "Rosy"},
            {"food": "Fresh Bread", "quantity": 30, "location": "Chennai", "urgency": "Normal", "donor_name": "Kumar"},
            {"food": "Fruits & Snacks", "quantity": 15, "location": "Chennai", "urgency": "Normal", "donor_name": "Asha"},
        ]

    cols = st.columns(3)
    emojis = ["🍛", "🥖", "🍎"]
    for i, item in enumerate(sample):
        with cols[i]:
            st.markdown(
                f"""
                <div class="food-card">
                    <div class="food-photo">{emojis[i % len(emojis)]}</div>
                    <div class="food-name">{item.get("food", "Food")}</div>
                    <div class="food-meta">🥗 {item.get("quantity", 0)} {t("meals")} • 📍 {item.get("location", "")}</div>
                    <div class="food-meta">♡ {t("donated_by")} {item.get("donor_name", "Donor")}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    total_meals = sum(int(d.get("quantity", 0) or 0) for d in load_donations())
    st1, st2, st3, st4 = st.columns(4)
    stats = [
        (total_meals or 1250, t("meals_helped")),
        (len(load_users()) or 850, t("people_helped")),
        (round((total_meals or 120) * 0.25), t("food_saved")),
        (sum(1 for u in load_users() if u.get("role") == "Donor") or 50, t("active_donors")),
    ]
    for col, (num, label) in zip([st1, st2, st3, st4], stats):
        with col:
            st.markdown(
                f'<div class="stat-box"><div class="stat-number">{num:,}+</div><div class="stat-label">{label}</div></div>',
                unsafe_allow_html=True,
            )


# =========================================================
# DONOR
# =========================================================

elif st.session_state.page == "Donor":
    st.markdown(f'<div class="page-title">{t("donor")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("donate_card_text")}</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        if not donor_exists():
            st.markdown(
                f"""
                <div class="form-card login-card">
                    <h2 style="font-family:Playfair Display;color:#0d4b37;">{t("first_time_donor")}</h2>
                    <p class="small-muted">{t("first_registration")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            name = st.text_input(t("username"), key="new_donor_name")
            email = st.text_input(t("email"), key="new_donor_email")
            phone = st.text_input(t("phone"), key="new_donor_phone")

            if st.button(t("create_account"), use_container_width=True):
                if not name.strip():
                    st.error(t("enter_name"))
                elif not valid_email(email):
                    st.error(t("valid_email"))
                elif not valid_phone(phone):
                    st.error(t("valid_phone"))
                else:
                    user = {
                        "role": "Donor",
                        "name": name.strip(),
                        "email": email.strip(),
                        "phone": re.sub(r"\D", "", phone),
                    }
                    users = load_users()
                    users.append(user)
                    save_users(users)
                    login_user(user)
                    st.success(t("account_created"))
                    st.rerun()

        else:
            st.markdown(
                f"""
                <div class="form-card login-card">
                    <h2 style="font-family:Playfair Display;color:#0d4b37;">{t("donor_login")}</h2>
                    <p class="small-muted">{t("welcome_back")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            name = st.text_input(t("username"), key="donor_login_name")
            if st.button(t("login"), use_container_width=True):
                user = find_donor(name)
                if user:
                    login_user(user)
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("name_not_found"))

    else:
        if st.session_state.role != "Donor":
            st.info("This section is for donors. You are currently logged in as a Receiver.")
        else:
            st.markdown(
                f"""
                <div class="hero">
                    <h2>{t("welcome_name", name=st.session_state.user_name)}</h2>
                    <p>{t("donate_card_text")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(f'<div class="section-title">{t("donor")}</div>', unsafe_allow_html=True)

            left, right = st.columns([1, 1.25])

            with left:
                st.markdown('<div class="form-card">', unsafe_allow_html=True)
                st.markdown(f"### 📷 {t('food_photo')}")
                st.file_uploader(
                    t("food_photo"),
                    type=["png", "jpg", "jpeg"],
                    label_visibility="collapsed",
                    key="food_image",
                )
                food_name = st.text_input(t("food_name"), placeholder="e.g. Cooked Rice & Vegetables")
                category = st.selectbox(
                    t("food_category"),
                    ["Vegetarian", "Meals", "Food"],
                )
                quantity = st.number_input(t("servings"), min_value=1, value=10, step=1)
                prepared_time = st.time_input(t("prepared_time"), value=datetime.now().time())
                expiry_date = st.date_input(t("expiry_date"))
                pickup_location = st.text_input(t("pickup_location"), placeholder="Chennai")
                notes = st.text_area(t("notes"), placeholder="Any special instructions...")
                st.markdown('</div>', unsafe_allow_html=True)

            with right:
                st.markdown(
                    f"""
                    <div class="soft-panel">
                        <b style="color:#0d4b37;">🧠 {t("nlp_analysis")}</b>
                        <p class="small-muted">Describe the donation below. Our NLP module will identify food type, quantity, location and urgency.</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                message = st.text_area(
                    t("food_description"),
                    placeholder="Example: We have 50 vegetarian meals left in Chennai. Please collect within 1 hour.",
                    height=150,
                    key="donation_message",
                )

                if st.button("🔍 " + t("analyze_find"), use_container_width=True):
                    if not message.strip():
                        st.error(t("describe_food"))
                    elif not pickup_location.strip():
                        st.error(t("enter_location"))
                    else:
                        result = analyze_food_message(message)
                        result["numbers"] = [str(quantity)]
                        result["locations"] = [pickup_location]

                        matches = find_matches(result)
                        st.session_state.last_matches = matches

                        food_types = result.get("food_types", [])
                        food_text = ", ".join(food_types) if food_types else category

                        donation = {
                            "id": datetime.now().strftime("%Y%m%d%H%M%S%f"),
                            "donor_name": st.session_state.user_name,
                            "donor_email": st.session_state.user_email,
                            "food": food_name.strip() if food_name.strip() else food_text,
                            "category": category,
                            "quantity": int(quantity),
                            "location": pickup_location.strip(),
                            "urgency": result.get("urgency", "Normal"),
                            "message": message.strip(),
                            "notes": notes.strip(),
                            "prepared_time": str(prepared_time),
                            "expiry_date": str(expiry_date),
                            "matches": matches,
                            "status": "Available",
                            "accepted_by": "",
                            "created_at": datetime.now().strftime("%d %b %Y • %I:%M %p"),
                        }

                        donations = load_donations()
                        donations.append(donation)
                        save_donations(donations)

                        st.success(t("donation_added"))

                        st.markdown(f'<div class="section-title">🧠 {t("nlp_analysis")}</div>', unsafe_allow_html=True)
                        a, b, c, d = st.columns(4)
                        values = [
                            (food_text, t("food_type")),
                            (quantity, t("quantity")),
                            (pickup_location, t("pickup_location")),
                            (result.get("urgency", "Normal"), t("urgency")),
                        ]
                        for col, (value, label) in zip([a, b, c, d], values):
                            with col:
                                st.markdown(
                                    f'<div class="stat-box"><div class="stat-number" style="font-size:18px">{value}</div><div class="stat-label">{label}</div></div>',
                                    unsafe_allow_html=True,
                                )

                        st.markdown(f'<div class="section-title">🎯 {t("suitable")}</div>', unsafe_allow_html=True)

                        if matches:
                            st.success(f"{len(matches)} {t('receiver_found')}")
                            for receiver in matches[:3]:
                                name = receiver.get("name", "Receiver")
                                location = receiver.get("location", pickup_location)
                                distance = receiver.get("distance", 5)
                                st.markdown(
                                    f"""
                                    <div class="noti-card">
                                        <b style="color:#0d4b37;">🏠 {name}</b>
                                        <div class="small-muted">📍 {location} &nbsp; • &nbsp; {distance} {t("distance")}</div>
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.warning(t("no_receiver"))


# =========================================================
# RECEIVER
# =========================================================

elif st.session_state.page == "Receiver":
    st.markdown(f'<div class="page-title">{t("find_food_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("find_food_sub")}</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        if not receiver_exists():
            st.markdown(
                f"""
                <div class="form-card login-card">
                    <h2 style="font-family:Playfair Display;color:#0d4b37;">{t("first_time_receiver")}</h2>
                    <p class="small-muted">{t("first_registration")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            name = st.text_input(t("username"), key="new_receiver_name")
            email = st.text_input(t("email"), key="new_receiver_email")
            phone = st.text_input(t("phone"), key="new_receiver_phone")
            trust_code = st.text_input(t("trust_code"), key="new_receiver_trust")

            if st.button(t("create_account"), use_container_width=True):
                if not name.strip():
                    st.error(t("enter_name"))
                elif not valid_email(email):
                    st.error(t("valid_email"))
                elif not valid_phone(phone):
                    st.error(t("valid_phone"))
                elif not trust_code.strip():
                    st.error(t("enter_trust"))
                elif trust_code_exists(trust_code):
                    st.error(t("trust_used"))
                else:
                    user = {
                        "role": "Receiver",
                        "name": name.strip(),
                        "email": email.strip(),
                        "phone": re.sub(r"\D", "", phone),
                        "trust_code": trust_code.strip(),
                    }
                    users = load_users()
                    users.append(user)
                    save_users(users)
                    login_user(user)
                    st.success(t("account_created"))
                    st.rerun()
        else:
            st.markdown(
                f"""
                <div class="form-card login-card">
                    <h2 style="font-family:Playfair Display;color:#0d4b37;">{t("receiver_login")}</h2>
                    <p class="small-muted">{t("welcome_back")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            name = st.text_input(t("username"), key="receiver_login_name")
            trust_code = st.text_input(t("trust_code"), key="receiver_login_trust")

            if st.button(t("login"), use_container_width=True):
                user = find_receiver(name, trust_code)
                if user:
                    login_user(user)
                    st.success(t("login_success"))
                    st.rerun()
                else:
                    st.error(t("wrong_receiver"))

    else:
        if st.session_state.role != "Receiver":
            st.info("This section is for receivers. You are currently logged in as a Donor.")
        else:
            st.markdown(
                f"""
                <div class="hero">
                    <h2>{t("find_food_title")}</h2>
                    <p>{t("find_food_sub")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            s1, s2, s3, s4 = st.columns([2.5, 1, 1, 1])
            with s1:
                search = st.text_input(" ", placeholder=t("search"), label_visibility="collapsed")
            with s2:
                st.selectbox(" ", [t("within"), "Within 10 km", "Within 20 km"], label_visibility="collapsed")
            with s3:
                st.selectbox(" ", [t("all_categories"), "Meals", "Food", "Vegetarian"], label_visibility="collapsed")
            with s4:
                st.selectbox(" ", [t("available_now"), "All"], label_visibility="collapsed")

            donations = [
                d for d in load_donations()
                if d.get("status", "Available") == "Available"
            ]

            if search.strip():
                q = search.lower()
                donations = [
                    d for d in donations
                    if q in str(d.get("food", "")).lower()
                    or q in str(d.get("location", "")).lower()
                    or q in str(d.get("donor_name", "")).lower()
                ]

            st.markdown('<div class="section-title">📍 Available Food</div>', unsafe_allow_html=True)

            if not donations:
                st.info(t("no_food"))
            else:
                for i, donation in enumerate(donations):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(
                            f"""
                            <div class="noti-card">
                                <div style="font-size:18px;font-weight:700;color:#0d4b37;">
                                    {"🍛" if i % 3 == 0 else "🥖" if i % 3 == 1 else "🍎"}
                                    {donation.get("food", "Food")}
                                </div>
                                <div class="small-muted">
                                    🥗 {donation.get("category", "Food")} &nbsp; • &nbsp;
                                    {donation.get("quantity", 0)} {t("meals")} &nbsp; • &nbsp;
                                    📍 {donation.get("location", "")}
                                </div>
                                <div class="small-muted">
                                    {t("donated_by")} {donation.get("donor_name", "Donor")}
                                    &nbsp; • &nbsp; <span class="badge">✓ {t("verified")}</span>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    with col2:
                        st.write("")
                        if st.button(t("request"), key=f"request_{donation.get('id', i)}", use_container_width=True):
                            all_donations = load_donations()
                            for item in all_donations:
                                if item.get("id") == donation.get("id"):
                                    item["status"] = "Accepted"
                                    item["accepted_by"] = st.session_state.user_name
                                    break
                            save_donations(all_donations)
                            st.session_state.notifications.insert(
                                0,
                                {
                                    "title": t("request_accepted"),
                                    "body": f"{donation.get('food', 'Food')} • {donation.get('quantity', 0)} {t('meals')}",
                                    "time": "Just now",
                                    "icon": "✓",
                                },
                            )
                            st.success(t("donation_accepted"))
                            st.info(t("donor_notified"))
                            st.rerun()


# =========================================================
# LANGUAGE
# =========================================================

elif st.session_state.page == "Language":
    st.markdown(
        f"""
        <div class="language-box">
            <div class="language-globe">◎</div>
            <div class="page-title" style="font-size:30px;">{t("language_title")}</div>
            <div class="page-subtitle">{t("language_sub")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    languages = ["English", "Tamil", "Hindi", "Telugu", "Malayalam", "Kannada"]
    selected = st.selectbox(
        " ",
        languages,
        index=languages.index(st.session_state.language),
        label_visibility="collapsed",
    )

    if selected != st.session_state.language:
        st.session_state.language = selected
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("✓  " + t("save_language"), use_container_width=True):
        st.success(f"{t('language_title')}: {st.session_state.language}")


# =========================================================
# NOTIFICATIONS
# =========================================================

elif st.session_state.page == "Notifications":
    st.markdown(f'<div class="page-title">{t("notification_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("notification_sub")}</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info(t("please_login"))
    else:
        notifications = list(st.session_state.notifications)

        donations = load_donations()
        for d in donations:
            if st.session_state.role == "Donor" and d.get("donor_name") == st.session_state.user_name and d.get("status") == "Accepted":
                notifications.append({
                    "title": t("request_accepted"),
                    "body": f'{d.get("food", "Food")} • {t("accepted")} by {d.get("accepted_by", "Receiver")}',
                    "time": d.get("created_at", "Recently"),
                    "icon": "✓",
                })
            elif st.session_state.role == "Receiver" and d.get("accepted_by") == st.session_state.user_name:
                notifications.append({
                    "title": t("donation_accepted"),
                    "body": f'{d.get("food", "Food")} • {d.get("donor_name", "Donor")}',
                    "time": d.get("created_at", "Recently"),
                    "icon": "♥",
                })

        # Keep unique notifications.
        unique = []
        seen = set()
        for n in notifications:
            key = (n.get("title"), n.get("body"))
            if key not in seen:
                seen.add(key)
                unique.append(n)

        if not unique:
            st.info(t("no_notifications"))
        else:
            icons = ["🎁", "✓", "📅", "♥", "💬"]
            for i, n in enumerate(unique):
                st.markdown(
                    f"""
                    <div class="noti-card">
                        <div style="display:flex;gap:13px;align-items:center;">
                            <div style="font-size:25px;">{n.get("icon", icons[i % len(icons)])}</div>
                            <div style="flex:1;">
                                <b style="color:#0d4b37;">{n.get("title", "Notification")}</b>
                                <div class="small-muted">{n.get("body", "")}</div>
                            </div>
                            <div class="small-muted">{n.get("time", "Now")}</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# =========================================================
# PROFILE
# =========================================================

elif st.session_state.page == "My Profile":
    st.markdown(f'<div class="page-title">{t("profile_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{t("good_food")}</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info(t("please_login"))
    else:
        donations = load_donations()
        my_donations = [
            d for d in donations
            if d.get("donor_name") == st.session_state.user_name
        ]
        accepted = [
            d for d in donations
            if d.get("accepted_by") == st.session_state.user_name
        ]

        total = len(my_donations) + len(accepted)
        helped = sum(int(d.get("quantity", 0) or 0) for d in my_donations)
        kg = round(helped * 0.25, 1)

        st.markdown(
            f"""
            <div class="profile-card">
                <div class="avatar">👩🏻</div>
                <div class="profile-name">{st.session_state.user_name}</div>
                <span class="badge">✓ {t("trusted_donor")}</span>
                <p class="small-muted">{t("good_food")}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        p1, p2, p3 = st.columns(3)
        for col, number, label in [
            (p1, total, t("donations")),
            (p2, helped, t("people_helped")),
            (p3, kg, t("kg_saved")),
        ]:
            with col:
                st.markdown(
                    f'<div class="stat-box"><div class="stat-number">{number}</div><div class="stat-label">{label}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="form-card">
                <b style="color:#0d4b37;">✉ Email</b><br>
                <span class="small-muted">{st.session_state.user_email}</span><br><br>
                <b style="color:#0d4b37;">☎ Phone</b><br>
                <span class="small-muted">+91 {st.session_state.phone}</span><br><br>
                <b style="color:#0d4b37;">📍 Location</b><br>
                <span class="small-muted">Chennai, Tamil Nadu</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


# =========================================================
# HISTORY
# =========================================================

elif st.session_state.page == "History":
    st.markdown(f'<div class="page-title">{t("history_title")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Track your donations and requests.</div>', unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.info(t("please_login"))
    else:
        donations = load_donations()
        if st.session_state.role == "Donor":
            records = [d for d in donations if d.get("donor_name") == st.session_state.user_name]
        else:
            records = [d for d in donations if d.get("accepted_by") == st.session_state.user_name]

        if not records:
            st.info(t("no_history"))
        else:
            for i, d in enumerate(reversed(records)):
                status = d.get("status", "Available")
                badge_class = "badge"
                st.markdown(
                    f"""
                    <div class="noti-card">
                        <div style="font-size:18px;font-weight:700;color:#0d4b37;">
                            {"🍛" if i % 3 == 0 else "🥖" if i % 3 == 1 else "🍎"}
                            {d.get("food", "Food")}
                        </div>
                        <div class="small-muted">
                            {d.get("quantity", 0)} {t("meals")} • {d.get("location", "")}
                        </div>
                        <div class="small-muted">
                            {d.get("created_at", "")}
                            &nbsp; • &nbsp;
                            <span class="{badge_class}">{status}</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


# =========================================================
# SETTINGS
# =========================================================

elif st.session_state.page == "Settings":
    st.markdown(f'<div class="page-title">{t("settings")}</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Simple controls for your Food Donor experience.</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="form-card">
            <h3 style="font-family:Playfair Display;color:#0d4b37;">Appearance</h3>
            <p class="small-muted">The Food Donor theme uses cream, forest green, sage and coral throughout the application.</p>
            <hr>
            <h3 style="font-family:Playfair Display;color:#0d4b37;">{t("privacy")}</h3>
            <p class="small-muted">Your local project stores account and donation data in JSON files inside the project folder.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🚪 " + t("logout"), use_container_width=True):
        logout_user()
        st.rerun()
