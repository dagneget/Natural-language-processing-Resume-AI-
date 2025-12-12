from src.screener import calculate_similarity

def test_calculate_similarity_exact_match():
    text1 = "Python developer with machine learning"
    text2 = "Python developer with machine learning"
    score = calculate_similarity(text1, text2)
    assert score > 99.0

def test_calculate_similarity_no_match():
    text1 = "Python developer"
    text2 = "Chef cooking food"
    score = calculate_similarity(text1, text2)
    # Score should be very low
    assert score < 20.0
