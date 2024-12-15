# Code generated from prompt 1
import sqlite3

# Code generated from prompt 2
def display_menu():
    print("\n--- Contact Book Menu ---")
    print("1. Add Contact")
    print("2. View All Contacts")
    print("3. Search Contacts")
    print("4. Delete Contact")
    print("5. Exit")
    return input("Enter your choice: ")

# Code generated from prompts 1 and 3
def add_contact(conn, cursor):
    name = input("Enter name: ")
    emails = input("Enter email(s) separated by comma: ").split(',')
    phones = input("Enter phone number(s) separated by comma: ").split(',')
    
    cursor.execute("INSERT INTO contacts (name) VALUES (?)", (name,))
    contact_id = cursor.lastrowid
    
    for email in emails:
        cursor.execute("INSERT INTO emails (contact_id, email) VALUES (?, ?)", (contact_id, email.strip()))
    
    for phone in phones:
        cursor.execute("INSERT INTO phones (contact_id, phone) VALUES (?, ?)", (contact_id, phone.strip()))
    
    conn.commit()
    print("Contact added successfully!")

# Code generated from additional prompt for viewing contacts
def view_all_contacts(cursor):
    cursor.execute("""
    SELECT c.id, c.name, GROUP_CONCAT(DISTINCT e.email) as emails, GROUP_CONCAT(DISTINCT p.phone) as phones
    FROM contacts c
    LEFT JOIN emails e ON c.id = e.contact_id
    LEFT JOIN phones p ON c.id = p.contact_id
    GROUP BY c.id
    """)
    contacts = cursor.fetchall()
    if contacts:
        for contact in contacts:
            print(f"ID: {contact[0]}, Name: {contact[1]}")
            print(f"Emails: {contact[2]}")
            print(f"Phones: {contact[3]}")
            print("------------------------")
    else:
        print("No contacts found.")

# Code generated from prompts 1 and 4
def search_contacts(cursor):
    search_term = input("Enter search term (name, email, or phone): ")
    cursor.execute("""
    SELECT DISTINCT c.id, c.name 
    FROM contacts c
    LEFT JOIN emails e ON c.id = e.contact_id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name LIKE ? OR e.email LIKE ? OR p.phone LIKE ?
    """, ('%'+search_term+'%', '%'+search_term+'%', '%'+search_term+'%'))
    results = cursor.fetchall()
    if results:
        for contact in results:
            print(f"ID: {contact[0]}, Name: {contact[1]}")
    else:
        print("No contacts found.")

# Code generated from prompt 1 and additional prompt for error handling
def delete_contact(conn, cursor):
    contact_id = input("Enter contact ID to delete: ")
    
    # First check if the contact exists
    cursor.execute("SELECT id FROM contacts WHERE id = ?", (contact_id,))
    if not cursor.fetchone():
        print("There is no contact to remove with that ID.")
        return
    
    # If contact exists, proceed with deletion
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    cursor.execute("DELETE FROM emails WHERE contact_id = ?", (contact_id,))
    cursor.execute("DELETE FROM phones WHERE contact_id = ?", (contact_id,))
    conn.commit()
    print("Contact deleted successfully!")

# Code generated from prompts 1 and 5
def main():
    conn = sqlite3.connect('contacts.db')
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts
                    (id INTEGER PRIMARY KEY, name TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS emails
                    (id INTEGER PRIMARY KEY, contact_id INTEGER, email TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS phones
                    (id INTEGER PRIMARY KEY, contact_id INTEGER, phone TEXT)''')
    
    while True:
        choice = display_menu()
        if choice == '1':
            add_contact(conn, cursor)
        elif choice == '2':
            view_all_contacts(cursor)
        elif choice == '3':
            search_contacts(cursor)
        elif choice == '4':
            delete_contact(conn, cursor)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
    
    conn.close()
    print("Thank you for using the Contact Book!")

if __name__ == "__main__":
    main()
