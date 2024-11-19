import random
"""
update this file to implement the following already declared methods:
- add_member: Should add a member to the self._members list
- delete_member: Should delete a member from the self._members list
- update_member: Should update a member from the self._members list
- get_member: Should return a member from the self._members list
"""
from random import randint

class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
        self._next_id = 1
        # example list of members
        self._members = []

    # read-only: Use this method to generate random members ID's when adding members into the list
    def _generateId(self):
        return random.randint(1,100)

    def add_member(self, member):
        # fill this method and update the return
          # Generar un ID único para el nuevo miembro
        member['id'] = self._generateId()  # Asignar un ID único al miembro
        member['last_name'] = self.last_name  # Asignar el apellido automáticamente
        self._members.append(member)
        

    def delete_member(self, id):
        # fill this method and update the return
       # Buscar el miembro por ID y eliminarlo
        member_to_remove = next((m for m in self._members if m['id'] == id), None)
        
        if member_to_remove:
            self._members.remove(member_to_remove)
        else:
            raise ValueError(f"Miembro con ID {id} no encontrado")
        
    def get_member(self, id):
        # fill this method and update the return
        member_finded = next((m for m in self._members if m['id'] == id), None)
        return member_finded
        

    # this method is done, it returns a list with all the family members
    def get_all_members(self):
        return self._members
