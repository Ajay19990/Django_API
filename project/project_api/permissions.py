from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
  """"Allow user to edit their profile."""
  # fefbce40bfe0750ff0bdfa66f9c9b910db89b355

  def has_object_permission(self, req, view, obj):
    """Check user is trying to edit their own profile."""

    # if obj.id != req.user.id and req.method in permissions.SAFE_METHODS:
      # return True
    # else:
    return obj.id == req.user.id