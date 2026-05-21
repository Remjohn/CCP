export function createQuizMachine(questions) {
    let currentIndex = 0;
    
    return {
        getCurrent: () => questions[currentIndex],
        answer: (isCorrect) => {
            if (isCorrect) {
                currentIndex++;
            }
            return isCorrect && currentIndex < questions.length;
        },
        isComplete: () => currentIndex >= questions.length
    };
}
