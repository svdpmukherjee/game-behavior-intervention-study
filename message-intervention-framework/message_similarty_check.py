from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load a pre-trained SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# List of messages
messages = [
    "What happens when you keep pushing yourself to improve? You start to see a pattern of success that proves you're capable. Can you think of a time when you worked hard and achieved something difficult - how did that make you feel about your abilities? That feeling of confidence comes from knowing you've overcome challenges before, and it's what will carry you through to even more accomplishments in the future.",
    "When you face a tough challenge, then you can look back at what you've already achieved. If you've solved similar problems before, then you know you have the skills to tackle this one. Your past successes show you what you're capable of, and that gives you the confidence to keep going. When you remember how you overcame obstacles in the past, then you can trust yourself to do it again.",
    "Genuine achievements feel different than fake ones. When you earn something through honest effort, it's like having a solid foundation beneath you. In contrast, taking shortcuts can feel like standing on shaky ground, where you're never really sure if you'll fall. Your past achievements are like building blocks that make you stronger and more confident.",
    "I look back on my journey and see how far I've come. Each challenge I've overcome is like a stepping stone to the next one. My past successes show me what I'm really capable of, and that helps me trust myself to keep moving forward. By focusing on my own achievements, I can see a clear path to future success.",
    "What does it take to feel truly confident in your abilities? It's the knowledge that you've earned your skills through hard work and dedication. Can you recall a time when you put in the effort to learn something new and it finally clicked? That sense of accomplishment is proof that you're capable of achieving authentic skill development.",
    "When you stick to your values and work hard, then you build a track record of genuine success. This shows you that you can trust yourself to get things done. If you've mastered skills before without taking shortcuts, then you know you can do it again. Your past achievements prove that you're capable, and that's what gives you the confidence to keep pushing forward.",
    "When you compare your successes to your struggles, you can see what works. Your past achievements show you what you're good at and what you need to work on. This helps you make better choices about where to focus your effort. By looking at what you've already accomplished, you can trust that you're on the right path.",
    "I think about the times I've struggled and still managed to succeed. Those moments prove to me that I have what it takes to handle tough situations. When I'm faced with a new challenge, I remind myself of the times I've come out on top through my own effort. This helps me trust that I can do it again, and that gives me the courage to keep going.",
    "What makes you think you can learn something new? \nIt's because you've already learned things before, right? \nYou can look back and see that you figured out tough stuff, and that shows you can do it again. \nDoesn't that make you feel more confident to take on the next challenge?",
    "When you work hard to develop a new skill, then you start to notice real progress. Your past achievements become a kind of map that shows you where you've been and what you can do. If you've successfully learned something before, then you can trust that you have the ability to learn it again. When you look back at what you've accomplished, then you can feel proud of your genuine growth over time."
  
    # (Include all messages here)
]

# Compute sentence embeddings
embeddings = model.encode(messages, convert_to_tensor=True)

# Compute cosine similarity matrix
semantic_similarity_matrix = cosine_similarity(embeddings.cpu().numpy())

# Compute average semantic similarity for each message
average_semantic_similarities = semantic_similarity_matrix.mean(axis=1)

# Rank messages by their average semantic similarity
ranked_semantic_messages = sorted(enumerate(average_semantic_similarities), key=lambda x: x[1], reverse=True)

# Print results
for rank, (index, score) in enumerate(ranked_semantic_messages, start=1):
    print(f"Rank {rank}: Message {index + 1} (Avg. Similarity: {score:.4f})")
