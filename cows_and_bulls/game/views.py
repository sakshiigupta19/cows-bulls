import random
from django.shortcuts import render
from django.http import JsonResponse

# Helper to generate a random 4-digit number with unique digits
def generate_number():
    return ''.join(random.sample("0123456789", 4))

# View for the main game page
def home(request):
    if 'secret_number' not in request.session:
        request.session['secret_number'] = generate_number()
        request.session['attempts_left'] = 10
        request.session['history'] = []
    return render(request, 'game/home.html')

# Check user's guess
def check_guess(request):
    if request.method == "POST":
        guess = request.POST.get('guess', '')
        secret_number = request.session.get('secret_number')
        attempts_left = request.session.get('attempts_left', 10)
        history = request.session.get('history', [])

        if len(guess) != 4 or len(set(guess)) != 4 or not guess.isdigit():
            return JsonResponse({'error': 'Invalid input. Enter a 4-digit number with unique digits.'}, status=400)

        # Calculate bulls and cows
        cows, bulls = 0, 0
        for i in range(4):
            if guess[i] == secret_number[i]:
                bulls += 1
            elif guess[i] in secret_number:
                cows += 1

        # Update history and attempts
        attempts_left -= 1
        result = f"{bulls}A{cows}B"
        history.append({'guess': guess, 'result': result})
        request.session['history'] = history
        request.session['attempts_left'] = attempts_left

        if bulls == 4:
            return JsonResponse({'message': 'You guessed it!', 'history': history})
        elif attempts_left == 0:
            return JsonResponse({'message': f'Game Over! The secret number was {secret_number}.', 'history': history,'attemptsLeft': attempts_left})

        return JsonResponse({'message': f'Cows: {cows}, Bulls: {bulls}', 'history': history,'attemptsLeft': attempts_left})

# Start a new game
def new_game(request):
    request.session['secret_number'] = generate_number()
    request.session['attempts_left'] = 10
    request.session['history'] = []
    print(f"New Secret Code: {request.session['secret_number']}")
    return JsonResponse({'message': 'New game started!', 'attemptsLeft': 10})