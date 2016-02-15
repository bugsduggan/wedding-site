var collapseRow = function() {
    $('tr.invitation-row', this).siblings().hide();
    $('div.owner-bottom', this).show();
};

var expandRow = function() {
    $('div.owner-bottom', this).hide();
    $('tr.invitation-row', this).siblings().show();
};

$(function() {
    $('table > tbody').hoverIntent({
        over: expandRow,
        out: collapseRow,
        timeout: 50
    });
    $('table > tbody').each(function() {
        collapseRow.call(this);
    });

    $('#delete-invitation-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var iid = button.data('invitation-iid');
        var deleteUrl = '/api/delete_invitation/' + iid;
        $('#delete-invitation-modal-delete-button').attr('href', deleteUrl);
    });

    $('#delete-user-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var uid = button.data('user-uid');
        var deleteUrl = '/api/delete_user/' + uid;
        $('#delete-user-modal-delete-button').attr('href', deleteUrl);
    });

    $('#add-user-modal-submit-button').on('click', function() {
        $('#add-user-form').submit();
    });
    $('#add-user-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var iid = button.data('invitation-iid');
        if (iid == 0) {
            // adding a new invitation, show size option
            $('#invitation-size-form-group').show();
            $('#invitation-status-form-group').show();
        } else {
            // adding a user to an existing invitation, no size needed
            $('#invitation-size-form-group').hide();
            $('#invitation-status-form-group').hide();
        }
        $('#invitation_iid').val(iid);
    });
    $('#add-user-modal').on('hidden.bs.modal', function() {
        $('#add-user-form').trigger('reset');
    });

    $('#change-response-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var uid = button.data('user-uid');
        var currentState = button.data('user-state');
        var confirmUrl = '/api/confirm_user/' + uid;
        var nullifyUrl = '/api/nullify_user/' + uid;
        var declineUrl = '/api/decline_user/' + uid;
        if (currentState == 0) {
            $('#change-response-confirm-button').prop('disabled', false);
            $('#change-response-nullify-button').prop('disabled', true);
            $('#change-response-decline-button').prop('disabled', false);
        } else if (currentState == 1) {
            $('#change-response-confirm-button').prop('disabled', true);
            $('#change-response-nullify-button').prop('disabled', false);
            $('#change-response-decline-button').prop('disabled', false);
        } else if (currentState == 2) {
            $('#change-response-confirm-button').prop('disabled', false);
            $('#change-response-nullify-button').prop('disabled', false);
            $('#change-response-decline-button').prop('disabled', true);
        } else {
            $('#change-response-confirm-button').prop('disabled', true);
            $('#change-response-nullify-button').prop('disabled', true);
            $('#change-response-decline-button').prop('disabled', true);
        }
        $('#change-response-confirm-button').off('click');
        $('#change-response-confirm-button').on('click', function() {
            window.location.href = confirmUrl;
        });
        $('#change-response-nullify-button').off('click');
        $('#change-response-nullify-button').on('click', function() {
            window.location.href = nullifyUrl;
        });
        $('#change-response-decline-button').off('click');
        $('#change-response-decline-button').on('click', function() {
            window.location.href = declineUrl;
        });
    });

    $('#change-invitation-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var iid = button.data('invitation-iid');
        var currentState = button.data('invitation-state');
        var dayUrl = '/api/invitation_day/' + iid;
        var eveningUrl = '/api/invitation_evening/' + iid;
        var bothUrl = '/api/invitation_both/' + iid;
        if (currentState == 1) {
            $('#change-invitation-day-button').prop('disabled', true);
            $('#change-invitation-evening-button').prop('disabled', false);
            $('#change-invitation-both-button').prop('disabled', false);
        } else if (currentState == 2) {
            $('#change-invitation-day-button').prop('disabled', false);
            $('#change-invitation-evening-button').prop('disabled', true);
            $('#change-invitation-both-button').prop('disabled', false);
        } else if (currentState == 3) {
            $('#change-invitation-day-button').prop('disabled', false);
            $('#change-invitation-evening-button').prop('disabled', false);
            $('#change-invitation-both-button').prop('disabled', true);
        } else {
            $('#change-invitation-day-button').prop('disabled', true);
            $('#change-invitation-evening-button').prop('disabled', true);
            $('#change-invitation-both-button').prop('disabled', true);
        }
        $('#change-invitation-day-button').off('click');
        $('#change-invitation-day-button').on('click', function() {
            window.location.href = dayUrl;
        });
        $('#change-invitation-evening-button').off('click');
        $('#change-invitation-evening-button').on('click', function() {
            window.location.href = eveningUrl;
        });
        $('#change-invitation-both-button').off('click');
        $('#change-invitation-both-button').on('click', function() {
            window.location.href = bothUrl;
        });
    });
});
