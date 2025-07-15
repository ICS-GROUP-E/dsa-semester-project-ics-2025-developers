class Graphs:
    def __init__(self):
        self.graph = {}

    def add_book_node(self, title):
        """Add a new book node to the graph"""
        if title not in self.graph:
            self.graph[title] = []
            return True
        return False

    def add_edge(self, book1, book2):
        """Connect two books as similar/related"""
        if book1 in self.graph and book2 in self.graph:
            if book2 not in self.graph[book1]:
                self.graph[book1].append(book2)
            if book1 not in self.graph[book2]:
                self.graph[book2].append(book1)
            return True
        return False

    def get_recommendations(self, title):
        """Get book recommendations using BFS traversal"""
        if title not in self.graph:
            return []

        visited = set()
        recommendations = []
        queue = [title]

        while queue:
            current_book = queue.pop(0)
            if current_book not in visited:
                visited.add(current_book)
                recommendations.append(current_book)
                for neighbor in self.graph[current_book]:
                    if neighbor not in visited:
                        queue.append(neighbor)

        # Remove the original book and return top 5 recommendations
        recommendations.remove(title)
        return recommendations[:5]

    def remove_book(self, title):
        """Remove a book and all its edges from the graph"""
        if title in self.graph:
            # Remove all edges to this book from other books
            for other_book in self.graph:
                if title in self.graph[other_book]:
                    self.graph[other_book].remove(title)
            # Remove the book itself
            del self.graph[title]
            return True
        return False

    def get_all_books(self):
        """Return list of all books in the graph"""
        return list(self.graph.keys())

    def get_similar_books(self, title):
        """Get directly connected similar books"""
        return self.graph.get(title, []) 