import random
import streamlit as st

def is_win(player, opponent):
    return (player == 'r' and opponent == 's') or \
           (player == 'p' and opponent == 'r') or \
           (player == 's' and opponent == 'p')

def play(user_choice):
    computer_choice = random.choice(['r', 'p', 's'])
    
    if user_choice == computer_choice:
        return 'tie', computer_choice
    
    if is_win(user_choice, computer_choice):
        return 'win', computer_choice
    
    return 'lose', computer_choice

st.title("Rock, Paper, Scissors Game")

# Session state for scores
if 'player_score' not in st.session_state:
    st.session_state.player_score = 0
if 'computer_score' not in st.session_state:
    st.session_state.computer_score = 0

user_choice = st.radio("Choose one:", ['r - Rock', 'p - Paper', 's - Scissors'])

if st.button("Play"):
    choice_letter = user_choice[0]  # Extract the first letter (r, p, or s)
    result, computer_choice = play(choice_letter)
    
    if result == 'win':
        st.session_state.player_score += 1
        st.success(f"You won! Computer chose {computer_choice}.")
    elif result == 'lose':
        st.session_state.computer_score += 1
        st.error(f"You lost! Computer chose {computer_choice}.")
    else:
        st.warning(f"It's a tie! Computer also chose {computer_choice}.")
    
st.write(f"**Your Score:** {st.session_state.player_score}")
st.write(f"**Computer Score:** {st.session_state.computer_score}")
