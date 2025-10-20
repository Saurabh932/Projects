# import random

def play_game(player, computer):
    if player == computer:
        return "It's a Tie!"
    elif (player == 'S' and computer == 'W') or \
         (player == 'W' and computer == 'G') or \
         (player == 'G' and computer == 'S'):
        return "You Win!"
    else:
        return "You Loose!"
    
# p1 = input("Select your move(S-Sanke, W-Watera and G-Gun): ").upper() 
# comp = random.choice(["S", "W", "G"])
# print(f"Computer chose: {comp}")

# print(play_game(p1,comp))