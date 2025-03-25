fruits = ['banana','mangoes','apples','oranges']

new_fruits = fruits

new_fruits.append('grapes')
print(fruits)
print(new_fruits)
new_fruits.remove('banana')
print(fruits)
print(new_fruits)
new_fruits.pop()
print(fruits)



invitees = ['Alice','Bob','Charlie','David']

def send_invitation(invitees):
    message = "You are invited to my party, "
    for invitee in invitees:
        print('\n',message + invitee)

send_invitation(invitees)
