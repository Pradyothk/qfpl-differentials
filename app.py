This is a great UX improvement. We will use `st.session_state` to manage which "Screen" is visible. This allows us to create a true **Splash Screen** experience and hide the tools until the user makes a choice.

Here is the updated `app.py`. I have updated the logic to start with a Home Screen, added "Back to Home" buttons on the tool pages, and filtered the phases to start from Phase 4.

### `app.py`

Copy this **entire** block into your GitHub file.

```python
import streamlit as st
import pandas as pd
import requests
import re
import io

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="QFPL Hub",
    page_icon="⚽",
    layout="wide"
)

# --- SESSION STATE SETUP (Navigation) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_home():
    st.session_state.page = 'home'

def go_diff():
    st.session_state.page = 'diff'

def go_help():
    st.session_state.page = 'help'

# --- EMBEDDED DATA ---
CSV_LINEUPS = """TEAM,PLAYER,TEAM,1,2,3,4,5,6,7
ARS,Arya Jain,ARS,S,S,S,C,,,
ARS,Dev Parikh,ARS,C,S,B,B,,,
ARS,Gaurav Gharge,ARS,S,S,B,S,,,
ARS,George Anagnostou,ARS,S,S,C,B,,,
ARS,Preet Chheda,ARS,S,B,S,S,,,
ARS,Preet Dedhia,ARS,S,B,S,S,,,
ARS,Saahil Sawant,ARS,B,B,S,S,,,
ARS,Shaad Lakdawala,ARS,B,S,B,S,,,
ARS,Shahmoon Ali Shah,ARS,B,C,S,B,,,
ARS,Tanuj Baru,ARS,B,B,S,S,,,
ARS,Timothy Leichtfried,ARS,S,S,B,B,,,
AVL,Abhiyank Choudhary,AVL,S,B,B,S,,,
AVL,Aditya Khullar,AVL,S,S,S,B,,,
AVL,Anson Rodrigues,AVL,S,S,B,B,,,
AVL,Avishek Das,AVL,B,C,S,S,,,
AVL,Darshil Shastri,AVL,S,S,B,B,,,
AVL,Debarun Guha,AVL,S,B,B,S,,,
AVL,Piyush Nathani,AVL,B,B,S,C,,,
AVL,Rishi Gehi,AVL,B,S,S,S,,,
AVL,Sagar Reddy,AVL,B,S,S,B,,,
AVL,Sarbik Dutta,AVL,C,S,S,S,,,
AVL,Sidharth Jain,AVL,S,B,C,S,,,
BOU,Akhil D,BOU,S,S,S,S,,,
BOU,Akshay Bhat,BOU,S,S,B,S,,,
BOU,Akshay Surve,BOU,B,C,S,B,,,
BOU,James Buller,BOU,C,B,S,B,,,
BOU,Kiran Kelkar,BOU,B,S,B,B,,,
BOU,Parth Mau,BOU,S,S,B,S,,,
BOU,Projwal Deb,BOU,B,S,S,B,,,
BOU,Rohit Ravi,BOU,B,B,S,S,,,
BOU,Vineet Udeshi,BOU,S,B,B,C,,,
BOU,Viral Panchal,BOU,S,B,S,S,,,
BOU,Vishnu Bhargav Janga,BOU,S,S,C,S,,,
BRE,Adit Maniktala,BRE,B,S,B,S,,,
BRE,Aman Arora,BRE,S,S,C,S,,,
BRE,Ashish Sharma,BRE,B,B,S,S,,,
BRE,Chandranil Mazumdar,BRE,S,B,S,C,,,
BRE,Harshal Bhungavale,BRE,S,B,B,S,,,
BRE,Mihir Pandya,BRE,S,C,S,B,,,
BRE,Mihir Ranade,BRE,B,S,S,B,,,
BRE,Mohar Moghe,BRE,S,S,B,S,,,
BRE,Rahul Vasu,BRE,B,S,B,S,,,
BRE,Siddharth Shenoy,BRE,S,S,S,B,,,
BRE,Umang Shah,BRE,C,B,S,B,,,
BHA,Abeen Bhattacharya,BHA,S,B,B,C,,,
BHA,Aditya Kalra,BHA,S,S,S,S,,,
BHA,Animesh Srivastava,BHA,B,S,S,B,,,
BHA,Anubhav Agarwal,BHA,S,B,S,B,,,
BHA,Harsh Ranjan,BHA,B,B,S,B,,,
BHA,Onas Malhotra,BHA,S,C,B,S,,,
BHA,Oni Malhotra,BHA,S,S,C,S,,,
BHA,Raghav Daga,BHA,C,S,B,B,,,
BHA,Shantanu Jha,BHA,B,B,S,S,,,
BHA,Swastik Dhopte,BHA,S,S,B,S,,,
BHA,Vivek Yadav,BHA,B,S,S,S,,,
BUR,Alissa Dsouza,BUR,S,B,S,C,,,
BUR,Amee Kapadia,BUR,B,S,S,B,,,
BUR,Anurag Khetan,BUR,B,S,S,S,,,
BUR,Delzad Bajan,BUR,S,S,B,S,,,
BUR,Jasprit Singh Sudan,BUR,C,S,B,S,,,
BUR,Rohan Ghosh,BUR,S,B,C,B,,,
BUR,Rudra Joshi,BUR,S,B,S,B,,,
BUR,Siddharth Nachankar,BUR,S,B,S,S,,,
BUR,Sidharth Nandwani,BUR,S,S,B,B,,,
BUR,Stefan Amanna,BUR,B,S,S,S,,,
BUR,Vaastav Anand,BUR,B,C,B,S,,,
CHE,Aarsh Mehta,CHE,C,S,B,S,,,
CHE,Abhigyan Khargharia,CHE,B,B,S,S,,,
CHE,Akshay Kumar,CHE,S,S,B,S,,,
CHE,Gaurab Kar,CHE,B,B,S,S,,,
CHE,Jay Shah,CHE,B,S,S,B,,,
CHE,Jay Vora,CHE,S,C,S,S,,,
CHE,Kowshik Suriyanarayanan,CHE,S,S,B,B,,,
CHE,Sushil Jadhav,CHE,S,B,C,S,,,
CHE,Varun Kumar,CHE,S,S,S,B,,,
CHE,Vishal Ananthakrishnan,CHE,S,S,B,B,,,
CHE,Vivek Merchant,CHE,B,B,S,C,,,
CRY,Adam Boustani,CRY,B,S,S,B,,,
CRY,Angelo Schellens,CRY,S,B,S,B,,,
CRY,Anshuman Dhanorkar,CRY,S,S,S,B,,,
CRY,Atinder Singh,CRY,S,S,B,C,,,
CRY,Maxilio John D'souza,CRY,B,C,B,S,,,
CRY,Mayur Bhatia,CRY,S,B,S,S,,,
CRY,Mayur Mishra,CRY,B,S,C,B,,,
CRY,Morrinho Pereira,CRY,B,S,B,S,,,
CRY,Rasendra Gaitonde,CRY,S,S,B,S,,,
CRY,Rohan Singhvi,CRY,C,B,S,S,,,
CRY,Shahbaz Anwer,CRY,S,B,S,S,,,
EVE,Amnay Sheel Khosla,EVE,B,S,B,B,,,
EVE,Dhruv Prasad,EVE,S,C,B,B,,,
EVE,Divyank Sharma,EVE,S,S,C,S,,,
EVE,Gaurav Partap Singh,EVE,S,B,B,S,,,
EVE,Kshitij Pandey,EVE,S,B,B,S,,,
EVE,Nikhil Narain,EVE,C,B,S,S,,,
EVE,Nilesh Agrawal,EVE,B,S,S,S,,,
EVE,Raghav Nath,EVE,S,S,S,B,,,
EVE,Sodaksh Khullar,EVE,B,B,S,B,,,
EVE,Somnath Dey,EVE,B,S,S,C,,,
EVE,Uddhav Prasad,EVE,S,S,S,S,,,
FUL,Arvind Mahesh,FUL,S,S,S,S,,,
FUL,Bharath Ravichandran,FUL,B,S,B,S,,,
FUL,Gandhar Badle,FUL,B,B,S,C,,,
FUL,Gurdit Singh Lugani,FUL,S,B,C,S,,,
FUL,Jai Kumar,FUL,B,S,S,S,,,
FUL,Karthik Easwar Elangovan,FUL,B,S,S,B,,,
FUL,Lv Shukla,FUL,C,B,S,B,,,
FUL,Pradyoth Kalavagunta,FUL,S,C,B,S,,,
FUL,Ramkumar Ananthakrishnan,FUL,S,B,S,B,,,
FUL,Surya Raman,FUL,S,S,B,B,,,
FUL,Vibudh Dixit,FUL,S,S,B,S,,,
LEE,Abhishek Pande,LEE,B,S,S,S,,,
LEE,Aliasgar Badami,LEE,B,B,S,B,,,
LEE,Haider Sayyed,LEE,S,B,B,S,,,
LEE,Jash Mehta,LEE,S,C,B,S,,,
LEE,Jay Lokegaonkar,LEE,B,S,B,C,,,
LEE,Muzzammil Peerbhai,LEE,C,S,S,S,,,
LEE,Ravi Jalan,LEE,S,B,S,B,,,
LEE,Sahil Bapat,LEE,S,B,S,S,,,
LEE,Shahid Nabi,LEE,S,S,S,S,,,
LEE,Siddharth Thakur,LEE,S,S,C,B,,,
LEE,Suraj Janyani,LEE,B,S,B,B,,,
LIV,Ajeesh VR,LIV,S,S,S,B,,,
LIV,Akshar,LIV,B,C,S,B,,,
LIV,Dhruv Kapur,LIV,B,B,S,C,,,
LIV,Navez Khan,LIV,B,S,S,S,,,
LIV,Prathmesh Rangari,LIV,B,B,S,S,,,
LIV,Rishabh Kothari,LIV,S,S,B,S,,,
LIV,Rishav Das,LIV,S,B,S,S,,,
LIV,Sanjeev Rai,LIV,S,B,C,S,,,
LIV,Shefal Chirawawala,LIV,S,S,B,B,,,
LIV,Varun S. Ranipeta,LIV,S,S,B,S,,,
LIV,Zubin Sheriar,LIV,C,S,B,B,,,
MCI,Abhimanyu Choudhury,MCI,C,B,B,S,,,
MCI,Abhinav Singh Sidhu,MCI,S,S,S,B,,,
MCI,Anirudh Shenoy,MCI,S,S,S,S,,,
MCI,Gokul Krishna,MCI,B,S,S,B,,,
MCI,Krishna Zanwar,MCI,B,C,B,S,,,
MCI,Nidhin Mathews,MCI,S,B,S,B,,,
MCI,Prathmesh Kocheta,MCI,S,B,B,C,,,
MCI,Raghav L Narasimhan,MCI,B,S,B,S,,,
MCI,Samson Baretto,MCI,S,S,S,B,,,
MCI,Saran Prasanth,MCI,S,B,S,S,,,
MCI,Sriram Ranganath,MCI,B,S,C,S,,,
MUN,Aaryan Rathi,MUN,S,B,B,C,,,
MUN,Ankur Mokal,MUN,S,C,S,S,,,
MUN,Anugreh Kumar,MUN,B,S,S,S,,,
MUN,Anuj Chandna,MUN,B,S,S,B,,,
MUN,Arijit Deb,MUN,S,S,B,B,,,
MUN,Lakshmi Narayanan,MUN,B,B,S,B,,,
MUN,Rahul Bhatu,MUN,B,S,B,B,,,
MUN,Rohan Singh,MUN,S,S,S,S,,,
MUN,Sheeraj Sengupta,MUN,S,B,S,S,,,
MUN,Utsav Ojha,MUN,C,B,B,S,,,
MUN,Yatin Mehra,MUN,S,S,C,S,,,
NEW,Akshat Jain,NEW,S,C,B,S,,,
NEW,Amitabh Agrawal,NEW,B,S,S,B,,,
NEW,Kinnari Vyas,NEW,B,S,B,S,,,
NEW,Piotr Kolodziej,NEW,S,S,S,S,,,
NEW,Prabhav VD,NEW,S,B,S,B,,,
NEW,Rahul VN,NEW,S,B,C,S,,,
NEW,Saswat Mishra,NEW,S,S,B,B,,,
NEW,Shashwat Mehrotra,NEW,B,S,B,S,,,
NEW,Siddharth Shinde,NEW,C,S,S,S,,,
NEW,Upamanyu Modukuru,NEW,B,B,S,C,,,
NEW,Vishnu Rajesh,NEW,S,B,S,B,,,
NFO,Ankur Goyal,NFO,S,S,C,S,,,
NFO,Arun Goyal,NFO,S,S,B,S,,,
NFO,Jay Bansal,NFO,S,B,B,S,,,
NFO,Prarabdh Chaturvedi,NFO,B,C,S,S,,,
NFO,Reuben Sam,NFO,B,B,S,B,,,
NFO,Shashank Jha,NFO,B,B,S,S,,,
NFO,Shiromi Chaturvedi,NFO,C,S,B,B,,,
NFO,Shubham Choudhary,NFO,S,S,S,B,,,
NFO,Soham Ghosh,NFO,B,S,S,S,,,
NFO,Swaroop Sarkar,NFO,S,S,B,C,,,
NFO,Vignesh Rajan,NFO,S,B,S,B,,,
SUN,Ajinkya Kale,SUN,B,S,C,B,,,
SUN,Avtansh Behal,SUN,S,B,S,S,,,
SUN,Ayanjit Chattopadhyay,SUN,S,B,S,C,,,
SUN,Kunal Soni,SUN,S,S,S,B,,,
SUN,Mohit Pant,SUN,S,S,B,S,,,
SUN,Priyan Gada,SUN,B,C,B,B,,,
SUN,Rajan Valecha,SUN,S,B,S,B,,,
SUN,Sanjay Krishna,SUN,B,S,S,S,,,
SUN,Snehasis Panda,SUN,C,B,B,S,,,
SUN,Sukhmani Singh,SUN,S,S,B,S,,,
SUN,Vishwa Jatania,SUN,B,S,S,S,,,
TOT,Aniket Neogi,TOT,B,S,B,C,,,
TOT,Aritra Mitra,TOT,S,S,B,S,,,
TOT,Ashwin Menon,TOT,S,B,S,B,,,
TOT,Kunal Bhatia,TOT,S,B,S,S,,,
TOT,Manan Vyas,TOT,C,B,S,S,,,
TOT,Mihir Vahi,TOT,B,S,C,B,,,
TOT,Pranav Mhatre,TOT,S,C,B,S,,,
TOT,Rahi Reza,TOT,B,B,S,S,,,
TOT,Ritobrata Nath,TOT,S,S,S,B,,,
TOT,Rohan Parekh,TOT,B,S,S,B,,,
TOT,Saksham Agarwal,TOT,S,S,B,S,,,
WHU,Advait Keswani,WHU,S,S,C,B,,,
WHU,Angad Singh,WHU,S,B,S,B,,,
WHU,Bhavika Anand,WHU,B,S,S,B,,,
WHU,Divij Ohri,WHU,S,C,B,S,,,
WHU,Harsh Rathod,WHU,S,S,S,S,,,
WHU,Jimmit Mehta,WHU,S,S,S,C,,,
WHU,Rujan Borges,WHU,S,B,B,S,,,
WHU,Sachin Omprakash,WHU,C,B,B,S,,,
WHU,Samarth Makhija,WHU,B,S,B,S,,,
WHU,Sreeradh RP,WHU,B,S,S,S,,,
WHU,Sriram Srinivasan,WHU,B,B,S,B,,,
WOL,Aksh Kapoor,WOL,S,B,S,B,,,
WOL,Gilson Rafael,WOL,S,S,B,S,,,
WOL,Hisham Ashraf,WOL,S,S,S,S,,,
WOL,Karan Manik,WOL,S,B,S,B,,,
WOL,Kashyap Reddy,WOL,B,S,B,C,,,
WOL,Kevin Sequeira,WOL,B,B,S,S,,,
WOL,Santosh Krishna,WOL,C,S,S,B,,,
WOL,Shekhar Perugu,WOL,S,S,C,S,,,
WOL,Sreekanth Reddy,WOL,S,B,S,S,,,
WOL,Vysakh Murali,WOL,B,C,B,S,,,
WOL,Yasser Rajwani,WOL,B,S,B,B,,,
"""

CSV_REGISTRATIONS = """Player,Profile
Jaidev Tripathy,https://fantasy.premierleague.com/entry/2395259/history
Jignesh Shah,https://fantasy.premierleague.com/entry/6472/history
Saurabh Wakode,https://fantasy.premierleague.com/entry/1158412/history
Simraan Panwar,https://fantasy.premierleague.com/entry/88361/history
Sumedh Garge,https://fantasy.premierleague.com/entry/226183/history
Udbhav Saha,https://fantasy.premierleague.com/entry/59794/history
Dhawal Lachhwani,https://fantasy.premierleague.com/entry/6980704/history
Daksha Iyer,https://fantasy.premierleague.com/entry/3729344/history
Saksham Arora,https://fantasy.premierleague.com/entry/2408693/history
Tanveer Singh,https://fantasy.premierleague.com/entry/4264/history
Arya Jain,https://fantasy.premierleague.com/entry/1221824/history
Dev Parikh,https://fantasy.premierleague.com/entry/25216/history
Gaurav Gharge,https://fantasy.premierleague.com/entry/13035/history
George Anagnostou,https://fantasy.premierleague.com/entry/11432/history
Preet Chheda,https://fantasy.premierleague.com/entry/478000/history
Preet Dedhia,https://fantasy.premierleague.com/entry/388983/history
Saahil Sawant,https://fantasy.premierleague.com/entry/4805767/history
Shaad Lakdawala,https://fantasy.premierleague.com/entry/82826/history
Shahmoon Ali Shah,https://fantasy.premierleague.com/entry/6003993/history
Tanuj Baru,https://fantasy.premierleague.com/entry/517401/history
Timothy Leichtfried,https://fantasy.premierleague.com/entry/97919/history
Abhiyank Choudhary,https://fantasy.premierleague.com/entry/12177/history
Aditya Khullar,https://fantasy.premierleague.com/entry/2411708/history
Anson Rodrigues,https://fantasy.premierleague.com/entry/4949507/history
Avishek Das,https://fantasy.premierleague.com/entry/20696/history
Darshil Shastri,https://fantasy.premierleague.com/entry/2123716/history
Debarun Guha,https://fantasy.premierleague.com/entry/10735/history
Piyush Nathani,https://fantasy.premierleague.com/entry/102225/history
Rishi Gehi,https://fantasy.premierleague.com/entry/17807/history
Sagar Reddy,https://fantasy.premierleague.com/entry/14059/history
Sarbik Dutta,https://fantasy.premierleague.com/entry/15515/history
Sidharth Jain,https://fantasy.premierleague.com/entry/11606/history
Akhil D,https://fantasy.premierleague.com/entry/43805/history
Akshay Bhat,https://fantasy.premierleague.com/entry/18604/history
Akshay Surve,https://fantasy.premierleague.com/entry/8287/history
James Buller,https://fantasy.premierleague.com/entry/47440/history
Kiran Kelkar,https://fantasy.premierleague.com/entry/52696/history
Parth Mau,https://fantasy.premierleague.com/entry/258145/history
Projwal Deb,https://fantasy.premierleague.com/entry/1661725/history
Rohit Ravi,https://fantasy.premierleague.com/entry/20159/history
Vineet Udeshi,https://fantasy.premierleague.com/entry/52860/history
Viral Panchal,https://fantasy.premierleague.com/entry/5679278/history
Vishnu Bhargav Janga,https://fantasy.premierleague.com/entry/23277/history
Adit Maniktala,https://fantasy.premierleague.com/entry/684711/history
Aman Arora,https://fantasy.premierleague.com/entry/15263/history
Ashish Sharma,https://fantasy.premierleague.com/entry/17924/history
Chandranil Mazumdar,https://fantasy.premierleague.com/entry/1004270/history
Harshal Bhungavale,https://fantasy.premierleague.com/entry/585313/history
Mihir Pandya,https://fantasy.premierleague.com/entry/3113/history
Mihir Ranade,https://fantasy.premierleague.com/entry/540994/history
Mohar Moghe,https://fantasy.premierleague.com/entry/155179/history
Rahul Vasu,https://fantasy.premierleague.com/entry/1385442/history
Siddharth Shenoy,https://fantasy.premierleague.com/entry/616635/history
Umang Shah,https://fantasy.premierleague.com/entry/33091/history
Abeen Bhattacharya,https://fantasy.premierleague.com/entry/284660/history
Aditya Kalra,https://fantasy.premierleague.com/entry/84713/history
Animesh Srivastava,https://fantasy.premierleague.com/entry/1025728/history
Anubhav Agarwal,https://fantasy.premierleague.com/entry/1696225/history
Harsh Ranjan,https://fantasy.premierleague.com/entry/8435808/history
Onas Malhotra,https://fantasy.premierleague.com/entry/5531280/history
Oni Malhotra,https://fantasy.premierleague.com/entry/5720051/history
Raghav Daga,https://fantasy.premierleague.com/entry/59430/history
Shantanu Jha,https://fantasy.premierleague.com/entry/4064159/history
Swastik Dhopte,https://fantasy.premierleague.com/entry/22241/history
Vivek Yadav,https://fantasy.premierleague.com/entry/457390/history
Alissa Dsouza,https://fantasy.premierleague.com/entry/20138/history
Amee Kapadia,https://fantasy.premierleague.com/entry/138917/history
Anurag Khetan,https://fantasy.premierleague.com/entry/717/history
Delzad Bajan,https://fantasy.premierleague.com/entry/533100/history
Jasprit Singh Sudan,https://fantasy.premierleague.com/entry/114747/history
Rohan Ghosh,https://fantasy.premierleague.com/entry/20125/history
Rudra Joshi,https://fantasy.premierleague.com/entry/1935169/history
Siddharth Nachankar,https://fantasy.premierleague.com/entry/59878/history
Sidharth Nandwani,https://fantasy.premierleague.com/entry/8023/history
Stefan Amanna,https://fantasy.premierleague.com/entry/5538/history
Vaastav Anand,https://fantasy.premierleague.com/entry/25600/history
Aarsh Mehta,https://fantasy.premierleague.com/entry/406181/history
Abhigyan Khargharia,https://fantasy.premierleague.com/entry/2348502/history
Akshay Kumar,https://fantasy.premierleague.com/entry/19690/history
Gaurab Kar,https://fantasy.premierleague.com/entry/582767/history
Jay Shah,https://fantasy.premierleague.com/entry/4601241/history
Jay Vora,https://fantasy.premierleague.com/entry/5527125/history
Kowshik Suriyanarayanan,https://fantasy.premierleague.com/entry/43814/history
Sushil Jadhav,https://fantasy.premierleague.com/entry/51278/history
Varun Kumar,https://fantasy.premierleague.com/entry/3475023/history
Vishal Ananthakrishnan,https://fantasy.premierleague.com/entry/1489728/history
Vivek Merchant,https://fantasy.premierleague.com/entry/5508577/history
Adam Boustani,https://fantasy.premierleague.com/entry/213/history
Angelo Schellens,https://fantasy.premierleague.com/entry/6293/history
Anshuman Dhanorkar,https://fantasy.premierleague.com/entry/2749549/history
Atinder Singh,https://fantasy.premierleague.com/entry/152104/history
Maxilio John D'souza,https://fantasy.premierleague.com/entry/5313/history
Mayur Bhatia,https://fantasy.premierleague.com/entry/261545/history
Mayur Mishra,https://fantasy.premierleague.com/entry/1369142/history
Morrinho Pereira,https://fantasy.premierleague.com/entry/415518/history
Rasendra Gaitonde,https://fantasy.premierleague.com/entry/676990/history
Rohan Singhvi,https://fantasy.premierleague.com/entry/1295/history
Shahbaz Anwer,https://fantasy.premierleague.com/entry/190195/history
Amnay Sheel Khosla,https://fantasy.premierleague.com/entry/4620665/history
Dhruv Prasad,https://fantasy.premierleague.com/entry/36206/history
Divyank Sharma,https://fantasy.premierleague.com/entry/20752/history
Gaurav Partap Singh,https://fantasy.premierleague.com/entry/380640/history
Kshitij Pandey,https://fantasy.premierleague.com/entry/118785/history
Nikhil Narain,https://fantasy.premierleague.com/entry/23896/history
Nilesh Agrawal,https://fantasy.premierleague.com/entry/7376251/history
Raghav Nath,https://fantasy.premierleague.com/entry/17267/history
Sodaksh Khullar,https://fantasy.premierleague.com/entry/7187173/history
Somnath Dey,https://fantasy.premierleague.com/entry/624342/history
Uddhav Prasad,https://fantasy.premierleague.com/entry/4623590/history
Arvind Mahesh,https://fantasy.premierleague.com/entry/582057/history
Bharath Ravichandran,https://fantasy.premierleague.com/entry/1176245/history
Gandhar Badle,https://fantasy.premierleague.com/entry/278608/history
Gurdit Singh Lugani,https://fantasy.premierleague.com/entry/2493619/history
Jai Kumar,https://fantasy.premierleague.com/entry/4518462/history
Karthik Easwar Elangovan,https://fantasy.premierleague.com/entry/20825/history
Lv Shukla,https://fantasy.premierleague.com/entry/14803/history
Pradyoth Kalavagunta,https://fantasy.premierleague.com/entry/7650/history
Ramkumar Ananthakrishnan,https://fantasy.premierleague.com/entry/331867/history
Surya Raman,https://fantasy.premierleague.com/entry/246433/history
Vibudh Dixit,https://fantasy.premierleague.com/entry/3447420/history
Abhishek Pande,https://fantasy.premierleague.com/entry/4597645/history
Aliasgar Badami,https://fantasy.premierleague.com/entry/3655696/history
Haider Sayyed,https://fantasy.premierleague.com/entry/3090420/history
Jash Mehta,https://fantasy.premierleague.com/entry/22127/history
Jay Lokegaonkar,https://fantasy.premierleague.com/entry/124380/history
Muzzammil Peerbhai,https://fantasy.premierleague.com/entry/335416/history
Ravi Jalan,https://fantasy.premierleague.com/entry/4318163/history
Sahil Bapat,https://fantasy.premierleague.com/entry/7165/history
Shahid Nabi,https://fantasy.premierleague.com/entry/5055362/history
Siddharth Thakur,https://fantasy.premierleague.com/entry/42966/history
Suraj Janyani,https://fantasy.premierleague.com/entry/397091/history
Ajeesh VR,https://fantasy.premierleague.com/entry/18276/history
Akshar,https://fantasy.premierleague.com/entry/423961/history
Dhruv Kapur,https://fantasy.premierleague.com/entry/5634833/history
Navez Khan,https://fantasy.premierleague.com/entry/1956257/history
Prathmesh Rangari,https://fantasy.premierleague.com/entry/897373/history
Rishabh Kothari,https://fantasy.premierleague.com/entry/824265/history
Rishav Das,https://fantasy.premierleague.com/entry/3564691/history
Sanjeev Rai,https://fantasy.premierleague.com/entry/89291/history
Shefal Chirawawala,https://fantasy.premierleague.com/entry/291367/history
Varun S. Ranipeta,https://fantasy.premierleague.com/entry/135398/history
Zubin Sheriar,https://fantasy.premierleague.com/entry/1093785/history
Abhimanyu Choudhury,https://fantasy.premierleague.com/entry/81424/history
Abhinav Singh Sidhu,https://fantasy.premierleague.com/entry/57382/history
Anirudh Shenoy,https://fantasy.premierleague.com/entry/23357/history
Gokul Krishna,https://fantasy.premierleague.com/entry/15772/history
Krishna Zanwar,https://fantasy.premierleague.com/entry/36717/history
Nidhin Mathews,https://fantasy.premierleague.com/entry/2534682/history
Prathmesh Kocheta,https://fantasy.premierleague.com/entry/5902896/history
Raghav L Narasimhan,https://fantasy.premierleague.com/entry/3612175/history
Samson Baretto,https://fantasy.premierleague.com/entry/29629/history
Saran Prasanth,https://fantasy.premierleague.com/entry/68554/history
Sriram Ranganath,https://fantasy.premierleague.com/entry/4659883/history
Aaryan Rathi,https://fantasy.premierleague.com/entry/6247622/history
Ankur Mokal,https://fantasy.premierleague.com/entry/5993/history
Anugreh Kumar,https://fantasy.premierleague.com/entry/45224/history
Anuj Chandna,https://fantasy.premierleague.com/entry/2954260/history
Arijit Deb,https://fantasy.premierleague.com/entry/3712849/history
Lakshmi Narayanan,https://fantasy.premierleague.com/entry/63959/history
Rahul Bhatu,https://fantasy.premierleague.com/entry/73538/history
Rohan Singh,https://fantasy.premierleague.com/entry/385369/history
Sheeraj Sengupta,https://fantasy.premierleague.com/entry/36660/history
Utsav Ojha,https://fantasy.premierleague.com/entry/29573/history
Yatin Mehra,https://fantasy.premierleague.com/entry/25972/history
Akshat Jain,https://fantasy.premierleague.com/entry/1309448/history
Amitabh Agrawal,https://fantasy.premierleague.com/entry/864413/history
Kinnari Vyas,https://fantasy.premierleague.com/entry/3915547/history
Piotr Kolodziej,https://fantasy.premierleague.com/entry/2802195/history
Prabhav VD,https://fantasy.premierleague.com/entry/157571/history
Rahul VN,https://fantasy.premierleague.com/entry/34230/history
Saswat Mishra,https://fantasy.premierleague.com/entry/15918/history
Shashwat Mehrotra,https://fantasy.premierleague.com/entry/4123513/history
Siddharth Shinde,https://fantasy.premierleague.com/entry/248794/history
Upamanyu Modukuru,https://fantasy.premierleague.com/entry/5113160/history
Vishnu Rajesh,https://fantasy.premierleague.com/entry/1443409/history
Ankur Goyal,https://fantasy.premierleague.com/entry/9555/history
Arun Goyal,https://fantasy.premierleague.com/entry/50683/history
Jay Bansal,https://fantasy.premierleague.com/entry/410700/history
Prarabdh Chaturvedi,https://fantasy.premierleague.com/entry/184328/history
Reuben Sam,https://fantasy.premierleague.com/entry/6389009/history
Shashank Jha,https://fantasy.premierleague.com/entry/3441192/history
Shiromi Chaturvedi,https://fantasy.premierleague.com/entry/26482/history
Shubham Choudhary,https://fantasy.premierleague.com/entry/14668/history
Soham Ghosh,https://fantasy.premierleague.com/entry/5913963/history
Swaroop Sarkar,https://fantasy.premierleague.com/entry/3884566/history
Vignesh Rajan,https://fantasy.premierleague.com/entry/5889697/history
Ajinkya Kale,https://fantasy.premierleague.com/entry/19906/history
Avtansh Behal,https://fantasy.premierleague.com/entry/13171/history
Ayanjit Chattopadhyay,https://fantasy.premierleague.com/entry/97348/history
Kunal Soni,https://fantasy.premierleague.com/entry/134351/history
Mohit Pant,https://fantasy.premierleague.com/entry/332497/history
Priyan Gada,https://fantasy.premierleague.com/entry/180199/history
Rajan Valecha,https://fantasy.premierleague.com/entry/6396565/history
Sanjay Krishna,https://fantasy.premierleague.com/entry/6786008/history
Snehasis Panda,https://fantasy.premierleague.com/entry/3832661/history
Sukhmani Singh,https://fantasy.premierleague.com/entry/143451/history
Vishwa Jatania,https://fantasy.premierleague.com/entry/5198677/history
Aniket Neogi,https://fantasy.premierleague.com/entry/1835336/history
Aritra Mitra,https://fantasy.premierleague.com/entry/34456/history
Ashwin Menon,https://fantasy.premierleague.com/entry/108039/history
Kunal Bhatia,https://fantasy.premierleague.com/entry/10177/history
Manan Vyas,https://fantasy.premierleague.com/entry/22671/history
Mihir Vahi,https://fantasy.premierleague.com/entry/33983/history
Pranav Mhatre,https://fantasy.premierleague.com/entry/13342/history
Rahi Reza,https://fantasy.premierleague.com/entry/113610/history
Ritobrata Nath,https://fantasy.premierleague.com/entry/13127/history
Rohan Parekh,https://fantasy.premierleague.com/entry/13754/history
Saksham Agarwal,https://fantasy.premierleague.com/entry/14035/history
Advait Keswani,https://fantasy.premierleague.com/entry/1382717/history
Angad Singh,https://fantasy.premierleague.com/entry/34863/history
Bhavika Anand,https://fantasy.premierleague.com/entry/1889364/history
Divij Ohri,https://fantasy.premierleague.com/entry/1172781/history
Harsh Rathod,https://fantasy.premierleague.com/entry/2371022/history
Jimmit Mehta,https://fantasy.premierleague.com/entry/150649/history
Rujan Borges,https://fantasy.premierleague.com/entry/5283997/history
Sachin Omprakash,https://fantasy.premierleague.com/entry/2167102/history
Samarth Makhija,https://fantasy.premierleague.com/entry/1512777/history
Sreeradh RP,https://fantasy.premierleague.com/entry/2175698/history
Sriram Srinivasan,https://fantasy.premierleague.com/entry/1223841/history
Aksh Kapoor,https://fantasy.premierleague.com/entry/81366/history
Gilson Rafael,https://fantasy.premierleague.com/entry/2377950/history
Hisham Ashraf,https://fantasy.premierleague.com/entry/22393/history
Karan Manik,https://fantasy.premierleague.com/entry/36144/history
Kashyap Reddy,https://fantasy.premierleague.com/entry/28384/history
Kevin Sequeira,https://fantasy.premierleague.com/entry/14974/history
Santosh Krishna,https://fantasy.premierleague.com/entry/14765/history
Shekhar Perugu,https://fantasy.premierleague.com/entry/5558797/history
Sreekanth Reddy,https://fantasy.premierleague.com/entry/331108/history
Vysakh Murali,https://fantasy.premierleague.com/entry/877548/history
Yasser Rajwani,https://fantasy.premierleague.com/entry/3589830/history
Divyansh Joshi,https://fantasy.premierleague.com/entry/
Jaskaran Singh,https://fantasy.premierleague.com/entry/
"""

# --- CACHED FUNCTIONS ---
@st.cache_data
def load_data():
    try:
        # Load Lineups
        df_lineups = pd.read_csv(io.StringIO(CSV_LINEUPS))
        
        # Clean columns: 0=Team, 1=Player, 3-9=Phases 1-7
        df_lineups = df_lineups.iloc[:, [0, 1, 3, 4, 5, 6, 7, 8, 9]]
        df_lineups.columns = ['Team', 'Player', '1', '2', '3', '4', '5', '6', '7']
        
        # Load Registrations
        df_reg = pd.read_csv(io.StringIO(CSV_REGISTRATIONS))
        
        def get_id(url):
            if pd.isna(url): return None
            match = re.search(r'entry/(\d+)', str(url))
            return int(match.group(1)) if match else None
        
        df_reg['FPL_ID'] = df_reg['Profile'].apply(get_id)
        
        # Merge
        master_df = pd.merge(df_lineups, df_reg[['Player', 'FPL_ID']], on='Player', how='left')
        return master_df
    except Exception as e:
        st.error(f"Data Error: {e}")
        return pd.DataFrame()

@st.cache_data
def get_fpl_elements():
    try:
        r = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
        data = r.json()
        elements = {p['id']: {'name': p['web_name'], 'team_id': p['team']} for p in data['elements']}
        teams = {t['id']: t['short_name'] for t in data['teams']}
        return elements, teams
    except:
        return {}, {}

def get_picks(fpl_id, gw):
    if not fpl_id or pd.isna(fpl_id): return []
    try:
        url = f"https://fantasy.premierleague.com/api/entry/{int(fpl_id)}/event/{gw}/picks/"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return [p['element'] for p in r.json()['picks']]
    except:
        pass
    return []

# --- APP START ---
df = load_data()
fpl_elements, fpl_teams = get_fpl_elements()

if df.empty:
    st.error("Could not load QFPL data.")
    st.stop()

teams_list = sorted(df['Team'].unique().tolist())

# --- NAVIGATION ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_home(): st.session_state.page = 'home'
def go_diff(): st.session_state.page = 'diff'
def go_help(): st.session_state.page = 'help'

# ==========================================
# PAGE: HOME (SPLASH SCREEN)
# ==========================================
if st.session_state.page == 'home':
    st.markdown("<h1 style='text-align: center;'>🏆 QFPL Hub</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Your companion for the Quarterly Fantasy Premier League</h4>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 **Compare Squads**")
        st.markdown("Check how your QFPL team stacks up against opponents based on live FPL points.")
        st.button("Go to Differential Calculator", on_click=go_diff, type="primary", use_container_width=True)
        
    with col2:
        st.info("📋 **Submit Lineup**")
        st.markdown("Validate your bench streaks and captaincy usage before submitting for the next phase.")
        st.button("Go to Lineup Helper", on_click=go_help, type="primary", use_container_width=True)

# ==========================================
# PAGE: DIFFERENTIAL CALCULATOR
# ==========================================
elif st.session_state.page == 'diff':
    st.button("🏠 Back to Home", on_click=go_home)
    st.header("📊 Differential Calculator")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        team_a = st.selectbox("Your Team", teams_list, key='t1')
    with c2:
        opp_list = [t for t in teams_list if t != team_a]
        team_b = st.selectbox("Opponent", opp_list, key='t2')
    with c3:
        phase = st.selectbox("Phase", ['1', '2', '3', '4', '5', '6', '7'], key='p1')
    with c4:
        gw = st.number_input("Gameweek", min_value=1, max_value=38, value=20, key='g1')

    if st.button("Calculate Differentials", type="primary", use_container_width=True):
        if team_a == team_b:
            st.warning("Select different teams!")
        else:
            progress_bar = st.progress(0, text="Analyzing squads...")
            
            def get_holdings(team_name, p_bar_start, p_bar_end):
                holdings = {}
                roster = df[(df['Team'] == team_name) & (df[phase].str.upper().isin(['S', 'C']))]
                total = len(roster)
                if total == 0: return {}
                
                for i, (_, row) in enumerate(roster.iterrows()):
                    progress = p_bar_start + ((i+1) / total * (p_bar_end - p_bar_start))
                    progress_bar.progress(int(progress), text=f"Fetching {team_name}: {row['Player']}")
                    multiplier = 2 if str(row[phase]).upper() == 'C' else 1
                    picks = get_picks(row['FPL_ID'], gw)
                    for pid in picks:
                        holdings[pid] = holdings.get(pid, 0) + multiplier
                return holdings

            h_a = get_holdings(team_a, 0, 50)
            h_b = get_holdings(team_b, 50, 100)
            progress_bar.empty()

            all_pids = set(h_a.keys()) | set(h_b.keys())
            results = []
            
            for pid in all_pids:
                net = h_a.get(pid, 0) - h_b.get(pid, 0)
                if net != 0:
                    p_info = fpl_elements.get(pid, {'name': 'Unknown', 'team_id': 0})
                    results.append({
                        'Player': p_info['name'],
                        'Team': fpl_teams.get(p_info['team_id'], '-'),
                        f'{team_a}': h_a.get(pid, 0),
                        f'{team_b}': h_b.get(pid, 0),
                        'Net Advantage': net
                    })

            if not results:
                st.success("Teams are perfectly matched! No differentials.")
            else:
                res_df = pd.DataFrame(results)
                res_df['abs'] = res_df['Net Advantage'].abs()
                res_df = res_df.sort_values('abs', ascending=False).drop(columns=['abs'])
                
                def highlight_net(val):
                    if val > 0: return 'background-color: #d1e7dd; color: black'
                    if val < 0: return 'background-color: #f8d7da; color: black'
                    return ''

                st.dataframe(res_df.style.applymap(highlight_net, subset=['Net Advantage']), use_container_width=True, hide_index=True)

# ==========================================
# PAGE: LINEUP HELPER
# ==========================================
elif st.session_state.page == 'help':
    st.button("🏠 Back to Home", on_click=go_home)
    st.header("📋 Lineup Helper")
    
    col_a, col_b = st.columns(2)
    with col_a:
        my_team = st.selectbox("Select Your Team", teams_list)
    with col_b:
        # UPDATED: Only Phases 4-7
        next_phase = st.selectbox("Upcoming Phase to Submit", [4, 5, 6, 7])

    roster = df[df['Team'] == my_team].copy()
    analysis = []
    
    for _, row in roster.iterrows():
        p_name = row['Player']
        
        # 1. Bench Streak Check
        must_start = False
        streak_msg = "OK"
        
        p_minus_1 = str(next_phase - 1)
        p_minus_2 = str(next_phase - 2)
        
        if p_minus_1 in df.columns and p_minus_2 in df.columns:
            val_1 = str(row[p_minus_1]).upper()
            val_2 = str(row[p_minus_2]).upper()
            if val_1 == 'B' and val_2 == 'B':
                must_start = True
                streak_msg = "⚠️ MUST START (2x Benched)"
        
        # 2. Captaincy Check
        cap_count = 0
        for i in range(1, next_phase):
            if str(i) in df.columns:
                if str(row[str(i)]).upper() == 'C':
                    cap_count += 1
        
        cap_status = "✅ Available"
        if cap_count >= 1:
            cap_status = "❌ Used"
        
        analysis.append({
            "Player": p_name,
            "Bench Status": streak_msg,
            "Captaincy Status": cap_status,
            "_sort": 0 if must_start else 1
        })
    
    df_analysis = pd.DataFrame(analysis).sort_values(by=['_sort', 'Player'])
    
    # 1. Warnings
    must_starts = df_analysis[df_analysis['_sort'] == 0]
    if not must_starts.empty:
        st.error(f"🚨 MANDATORY SELECTION: These players MUST start:")
        for p in must_starts['Player']:
            st.markdown(f"- **{p}**")
    else:
        st.success("✅ No bench streak violations imminent.")

    st.divider()
    st.subheader("Squad Status")
    
    # 2. Table with Styling
    def highlight_rows(row):
        styles = []
        if row['_sort'] == 0:
            return ['background-color: #f8d7da; font-weight: bold'] * len(row)
        elif row['Captaincy Status'] == "❌ Used":
            return ['background-color: #fff3cd'] * len(row)
        else:
            return [''] * len(row)

    st.dataframe(
        df_analysis.style
        .apply(highlight_rows, axis=1)
        .hide(subset=['_sort'], axis='columns'),
        use_container_width=True,
        hide_index=True
    )
    
    st.divider()
    url = "https://docs.google.com/forms/d/e/1FAIpQLSfIPWcBe5LpLmI8dq5Jqxvw2ug9_9d2Ha9RIyREMEiBbNmyzQ/viewform?usp=header"
    st.link_button("🚀 Go to Submission Form", url, type="primary")

```
