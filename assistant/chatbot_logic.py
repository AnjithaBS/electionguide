def process_message(message, state):
    current_step = state.get('step', 'start')
    
    response = {
        'messages': [],
        'options': [],
        'state': state
    }

    if current_step == 'start':
        response['messages'] = [
            "Namaste! I am Election Guide India.",
            "I'm here to help you get ready for the elections.",
            "First, tell me: Is this your first time voting?"
        ]
        response['options'] = [
            {'label': 'Yes, it is!', 'action': 'first_time_yes'},
            {'label': 'No, I have voted before', 'action': 'first_time_no'}
        ]
        response['state']['step'] = 'ask_state'
        response['progress'] = {'step': 1, 'label': 'User Info'}

    elif current_step == 'ask_state':
        if message == 'first_time_yes':
            response['messages'] = ["Welcome! We love first-time voters. We will make sure you have all the information you need."]
            response['state']['is_first_time'] = True
        else:
            response['messages'] = ["Great! Welcome back. It's always good to stay updated on the process."]
            response['state']['is_first_time'] = False
            
        response['messages'].append("Which state or union territory are you from?")
        response['options'] = [
            {'label': 'Detect my location', 'action': 'location_detected', 'type': 'location'},
            {'label': 'Delhi', 'action': 'Delhi'},
            {'label': 'Maharashtra', 'action': 'Maharashtra'},
            {'label': 'Uttar Pradesh', 'action': 'Uttar Pradesh'},
            {'label': 'Karnataka', 'action': 'Karnataka'},
            {'label': 'Other (Type it manually)', 'action': 'ask_custom_state'}
        ]
        response['state']['step'] = 'handle_state_choice'
        response['progress'] = {'step': 1, 'label': 'User Info'}

    elif current_step == 'handle_state_choice':
        if message == 'location_error':
            response['messages'] = ["I couldn't detect your location. Please select or type your state:"]
            response['options'] = [
                {'label': 'Delhi', 'action': 'Delhi'},
                {'label': 'Maharashtra', 'action': 'Maharashtra'},
                {'label': 'Other', 'action': 'ask_custom_state'}
            ]
            response['state']['step'] = 'handle_state_choice'
            response['progress'] = {'step': 1, 'label': 'User Info'}
        elif message == 'ask_custom_state':
            response['messages'] = ["Please type the name of your state or union territory:"]
            response['options'] = [
                {'type': 'text_input', 'action': 'custom_state_entered', 'placeholder': 'Enter your state...'}
            ]
            response['state']['step'] = 'handle_state_choice'
            response['progress'] = {'step': 1, 'label': 'User Info'}
        else:
            # We got the state name, either from a button, text input, or location
            if message == 'location_detected':
                 response['state']['user_state'] = "Detected Location"
            else:
                 response['state']['user_state'] = message
            response['state']['user_state'] = message
            response['messages'] = ["What would you like help with today?"]
            response['options'] = [
                {'label': 'How elections work in India', 'action': 'elections_work'},
                {'label': 'How to vote (Checklist)', 'action': 'how_to_vote'},
                {'label': 'Important dates & deadlines', 'action': 'dates'},
                {'label': 'Voter ID & registration help', 'action': 'registration'},
                {'label': 'Voting assistance (PwD / Senior)', 'action': 'assistance'},
                {'label': 'Common Q&A', 'action': 'qa_menu'},
                {'label': 'Myth vs Fact', 'action': 'myth_vs_fact'}
            ]
            response['state']['step'] = 'handle_menu_choice'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

    elif current_step == 'main_menu':
        response['messages'] = ["What would you like help with today?"]
        response['options'] = [
            {'label': 'How elections work in India', 'action': 'elections_work'},
            {'label': 'How to vote (Checklist)', 'action': 'how_to_vote'},
            {'label': 'Important dates & deadlines', 'action': 'dates'},
            {'label': 'Voter ID & registration help', 'action': 'registration'},
            {'label': 'Voting assistance (PwD / Senior)', 'action': 'assistance'},
            {'label': 'Common Q&A', 'action': 'qa_menu'},
            {'label': 'Myth vs Fact', 'action': 'myth_vs_fact'}
        ]
        response['state']['step'] = 'handle_menu_choice'
        response['progress'] = {'step': 2, 'label': 'Guidance'}

    elif current_step == 'handle_menu_choice':
        if message == 'elections_work':
            response['messages'] = [
                "Here is how elections work in India:",
                "1. **Voter Registration**: Citizens aged 18+ must register with the Election Commission of India (ECI).",
                "2. **Candidates & Campaigns**: Political parties nominate candidates who campaign to reach voters.",
                "3. **Voting Process**: Voting happens using EVM (Electronic Voting Machine).",
                "  * **VVPAT**: Your vote is verified by a VVPAT slip shown for 7 seconds in a sealed window.",
                "4. **Vote Counting**: Votes are counted securely under ECI supervision.",
                "5. **Results**: Candidate with the highest votes wins.",
                "Would you like to check your voter registration or find your polling booth?"
            ]
            response['options'] = [
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['state']['step'] = 'main_menu'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'how_to_vote':
            response['messages'] = ["Let's check your readiness. Are you registered as a voter?"]
            response['options'] = [
                {'label': '✅ Yes', 'action': 'vote_step_2'},
                {'label': '❓ Not sure', 'action': 'check_registration_help'},
                {'label': '❌ No', 'action': 'registration'}
            ]
            response['state']['step'] = 'handle_menu_choice'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'check_registration_help':
            response['messages'] = [
                "You can easily check if your name is on the voter list.",
                "Would you like to visit the NVSP portal to search for your name?"
            ]
            response['options'] = [
                {'label': '🌐 Go to NVSP Portal', 'action': 'https://electoralsearch.eci.gov.in/', 'type': 'link'},
                {'label': '⬅️ Back to Checklist', 'action': 'how_to_vote'}
            ]
            response['state']['step'] = 'handle_menu_choice'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'vote_step_2':
             response['state']['is_registered'] = True
             response['messages'] = ["Great! Next, do you have your Voter ID (EPIC) or another valid ID ready?"]
             response['options'] = [
                 {'label': '✅ Yes', 'action': 'vote_step_3'},
                 {'label': '❌ No', 'action': 'registration'}
             ]
             response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'vote_step_3':
             response['state']['has_id'] = True
             response['messages'] = ["Awesome. Finally, do you know the exact location of your polling booth?"]
             response['options'] = [
                 {'label': '✅ Yes', 'action': 'vote_step_complete'},
                 {'label': '❓ Not sure / No', 'action': 'booth_help'}
             ]
             response['progress'] = {'step': 2, 'label': 'Guidance'}
             
        elif message == 'booth_help':
             response['messages'] = [
                 "You can find your exact polling booth details on the Voter Helpline App or NVSP website.",
                 "Would you like to check now?"
             ]
             response['options'] = [
                 {'label': '📱 Open Voter Helpline App', 'action': 'https://www.eci.gov.in/voter-helpline-app', 'type': 'link'},
                 {'label': '⬅️ Back to Checklist', 'action': 'vote_step_3'}
             ]
             response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'vote_step_complete':
             response['state']['knows_booth'] = True
             response['messages'] = [
                 "Excellent! You are fully prepared to vote.",
                 "On voting day, remember to cast your vote using the EVM and verify it with the VVPAT slip.",
                 "What would you like to do next?"
             ]
             response['options'] = [
                 {'label': '🏠 Home', 'action': 'main_menu'}
             ]
             response['progress'] = {'step': 3, 'label': 'Readiness'}

        elif message == 'dates':
            response['messages'] = [
                "Here are the important phases of an election:",
                "- **Announcement**: Election dates are announced by the ECI.",
                "- **Registration**: Registration deadlines usually close a few weeks before voting.",
                "- **Campaign**: Candidates campaign, ending 48 hours before polling.",
                "- **Voting**: Voting days (may happen in multiple phases).",
                "- **Results**: Votes are counted and results are declared.",
                "**IMPORTANT**: Election dates change and are officially announced by the Election Commission of India. Always check the latest schedule on the official ECI website."
            ]
            response['options'] = [{'label': '🏠 Home', 'action': 'main_menu'}]
            response['state']['step'] = 'main_menu'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'registration':
            response['messages'] = [
                "**Voter ID & Registration Help**",
                "You can apply online, track your application, or correct details using official portals.",
                "Required documents generally include Proof of Age and Proof of Address."
            ]
            response['options'] = [
                {'label': '🌐 Go to NVSP Portal', 'action': 'https://voters.eci.gov.in/', 'type': 'link'},
                {'label': '📱 Open Voter Helpline App', 'action': 'https://www.eci.gov.in/voter-helpline-app', 'type': 'link'},
                {'label': '🔍 Check Voter List', 'action': 'https://electoralsearch.eci.gov.in/', 'type': 'link'},
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['state']['step'] = 'main_menu'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'assistance':
            response['messages'] = [
                "**Voting Assistance (PwD & Senior Citizens)**",
                "- Wheelchair access is mandatory at polling stations.",
                "- Assistance by polling staff or volunteers is available.",
                "- Option for home voting exists in certain cases for seniors (85+) and PwD.",
                "- Transport or pick-up facilities are provided in some regions.",
                "Do you need specific assistance for voting?"
            ]
            response['options'] = [
                {'label': '✅ Yes, I need help', 'action': 'need_assistance_yes'},
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'need_assistance_yes':
            response['messages'] = [
                "Please contact your Booth Level Officer (BLO) or use the Saksham App by ECI to request specific assistance like home voting or wheelchair access before election day."
            ]
            response['options'] = [
                {'label': '📱 Saksham App', 'action': 'https://play.google.com/store/apps/details?id=pwd.eci.com.pwdapp', 'type': 'link'},
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['state']['step'] = 'main_menu'
            response['progress'] = {'step': 2, 'label': 'Guidance'}

        elif message == 'qa_menu':
            response['messages'] = ["What would you like to know?"]
            response['options'] = [
                {'label': 'Do I need Voter ID to vote?', 'action': 'qa_id'},
                {'label': 'What if my name is not in the voter list?', 'action': 'qa_list'},
                {'label': 'Can I vote from another city?', 'action': 'qa_city'},
                {'label': 'What is NOTA?', 'action': 'qa_nota'},
                {'label': 'What is EVM and VVPAT?', 'action': 'qa_evm'},
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['progress'] = {'step': 2, 'label': 'Guidance'}
        
        elif message == 'qa_id':
            response['messages'] = ["**Do I need a Voter ID to vote?**", "No. While Voter ID (EPIC) is preferred, you can use other approved IDs like Aadhaar, PAN Card, Driving License, or Passport, provided your name is on the voter list."]
            response['options'] = [{'label': '⬅️ More Q&A', 'action': 'qa_menu'}, {'label': '🏠 Home', 'action': 'main_menu'}]
        elif message == 'qa_list':
            response['messages'] = ["**What if my name is not in the voter list?**", "You cannot vote. It is mandatory for your name to be on the voter list of your polling booth, even if you have a Voter ID."]
            response['options'] = [{'label': '⬅️ More Q&A', 'action': 'qa_menu'}, {'label': '🏠 Home', 'action': 'main_menu'}]
        elif message == 'qa_city':
            response['messages'] = ["**Can I vote from another city?**", "No. You must vote at the specific polling booth where you are registered. You cannot vote online or from another city (unless you are a registered service voter)."]
            response['options'] = [{'label': '⬅️ More Q&A', 'action': 'qa_menu'}, {'label': '🏠 Home', 'action': 'main_menu'}]
        elif message == 'qa_nota':
            response['messages'] = ["**What is NOTA?**", "NOTA stands for 'None of the Above'. It allows you to officially register a vote of rejection for all candidates contesting in your constituency."]
            response['options'] = [{'label': '⬅️ More Q&A', 'action': 'qa_menu'}, {'label': '🏠 Home', 'action': 'main_menu'}]
        elif message == 'qa_evm':
            response['messages'] = ["**What is EVM and VVPAT?**", "EVM is the Electronic Voting Machine used to cast votes. VVPAT is a printer attached to the EVM that shows a paper slip for 7 seconds to verify your vote was recorded correctly."]
            response['options'] = [{'label': '⬅️ More Q&A', 'action': 'qa_menu'}, {'label': '🏠 Home', 'action': 'main_menu'}]

        elif message == 'myth_vs_fact':
            response['messages'] = ["Here are some common voting myths debunked. Which one would you like to explore?"]
            response['options'] = [
                {'label': 'Myth: Voter ID is mandatory', 'action': 'myth_id'},
                {'label': 'Myth: My vote doesn’t matter', 'action': 'myth_matter'},
                {'label': '🏠 Home', 'action': 'main_menu'}
            ]
            response['progress'] = {'step': 2, 'label': 'Guidance'}
        
        elif message == 'myth_id':
            response['messages'] = [
                "**Myth:** You absolutely need a Voter ID (EPIC) to cast your vote.",
                "**Fact:** Other approved IDs (like Aadhar, PAN, Passport) are also accepted, as long as your name is on the electoral roll."
            ]
            response['options'] = [{'label': '⬅️ Other Myths', 'action': 'myth_vs_fact'}, {'label': '🏠 Home', 'action': 'main_menu'}]
        elif message == 'myth_matter':
            response['messages'] = [
                "**Myth:** My single vote doesn't make any difference.",
                "**Fact:** Many elections, especially at the local and state levels, are decided by very small margins. Every single vote counts towards shaping the government."
            ]
            response['options'] = [{'label': '⬅️ Other Myths', 'action': 'myth_vs_fact'}, {'label': '🏠 Home', 'action': 'main_menu'}]

        else:
            response['messages'] = ["I didn't quite catch that. Let's return to the main menu."]
            response['options'] = [{'label': '🏠 Home', 'action': 'main_menu'}]
            response['state']['step'] = 'main_menu'

    # Catch-all
    if not response['messages']:
        response['messages'] = ["Let's start over."]
        response['options'] = [{'label': 'Start', 'action': 'start'}]
        response['state']['step'] = 'start'

    return response
