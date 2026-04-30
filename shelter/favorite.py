class Favorite:
    def __init__(self, request):
        self.session = request.session
        favorites = self.session.get('favorite_animals')
        if not favorites:
            favorites = self.session['favorite_animals'] = {}
        self.favorites = favorites

    def __len__(self):
        return len(self.favorites)

    def __iter__(self):
        return iter(self.favorites.values())

    def __contains__(self, animal_id):
        return str(animal_id) in self.favorites

    def __gt__(self, other):
        return len(self) > len(other)

    def __lt__(self, other):
        return len(self) < len(other)

    def __eq__(self, other):
        return len(self) == len(other)

    def __bool__(self):
        return len(self) > 0

    def __repr__(self):
        return f"Favorites({list(self.favorites.keys())})"

    def __str__(self):
        names = [item['name'] for item in self.favorites.values()]
        return f"Favorites: {', '.join(names)}" if names else "Favorites: (empty)"

    # --- Class-specific methods ---

    def add(self, animal):
        """Add an animal to favorites."""
        animal_id = str(animal.id)
        if animal_id not in self.favorites:
            self.favorites[animal_id] = {
                'id': animal.id,
                'name': animal.name,
                'species': animal.species,
            }
            self.save()

    def remove(self, animal):
        """Remove an animal from favorites."""
        animal_id = str(animal.id)
        if animal_id in self.favorites:
            del self.favorites[animal_id]
            self.save()

    def toggle(self, animal):
        """Add if not favorited, remove if already favorited."""
        if animal in self:
            self.remove(animal)
        else:
            self.add(animal)

    def save(self):
        """Mark the session as modified so Django saves it."""
        self.session.modified = True

    def clear(self):
        """Remove all favorites from the session."""
        self.session['favorite_animals'] = {}
        self.favorites = self.session['favorite_animals']
        self.save()

    def get_ids(self):
        """Return a list of integer IDs for database querying."""
        return [int(k) for k in self.favorites.keys()]