Library Project
# Permissions and Groups Setup Documentation

## Overview
This Django application implements a role-based access control system using custom permissions and user groups to manage access to Book resources.

## Custom Permissions

The Book model has four custom permissions defined:

1. **can_view** - Allows viewing book listings
2. **can_create** - Allows creating new books
3. **can_edit** - Allows editing existing books
4. **can_delete** - Allows deleting books

These permissions are defined in the Book model's Meta class in `models.py`.

## User Groups

Three groups have been created with different permission levels:

### Viewers Group
- **Permissions:** can_view
- **Purpose:** Users who can only view book information
- **Use Case:** General users, customers, or readers

### Editors Group
- **Permissions:** can_view, can_create, can_edit
- **Purpose:** Users who can manage book content but not delete
- **Use Case:** Content managers, librarians, staff members

### Admins Group
- **Permissions:** can_view, can_create, can_edit, can_delete
- **Purpose:** Users with full access to all book operations
- **Use Case:** Administrators, managers

## Views Protected by Permissions

The following views are protected:

- `book_list`: Requires `can_view` permission
- `book_create`: Requires `can_create` permission
- `book_edit`: Requires `can_edit` permission
- `book_delete`: Requires `can_delete` permission

All views also require users to be logged in (`@login_required` decorator).

## How to Assign Users to Groups

1. Access Django Admin at `/admin/`
2. Navigate to Users
3. Select a user
4. Scroll to "Groups" section
5. Select appropriate group(s)
6. Save

## Testing the Setup

To test permissions:
1. Create test users
2. Assign them to different groups
3. Log in as each user
4. Attempt to access different views
5. Verify that access is granted/denied appropriately

## Error Handling

Users without proper permissions will receive a 403 Forbidden error when attempting to access protected views.