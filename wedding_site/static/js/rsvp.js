$(function() {
    $('#dietary-requirements-modal-submit-button').on('click', function() {
        $('#update-dietary-requirements-form').submit();
    });
    
    $('#delete-guest-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var uid = button.data('user-uid');
        var userName = button.data('user-username');
        var deleteGuestUrl = '/delete_guest/' + uid;
        $('#delete-guest-modal-name').text(userName);
        $('#delete-guest-modal-delete-button').off('click');
        $('#delete-guest-modal-delete-button').on('click', function() {
            window.location.href = deleteGuestUrl;
        });
    });

    $('#add-user-modal-submit-button').on('click', function() {
        $('#add-user-form').submit();
    });
});
