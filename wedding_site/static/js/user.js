$(function() {
    $('#edit-name-modal-submit-button').on('click', function() {
        $('#edit-name-form').submit();
    });

    $('#dietary-requirements-modal-submit-button').on('click', function() {
        $('#update-dietary-requirements-form').submit();
    });

    $('#group-modal-submit-button').on('click', function() {
        $('#add-group-form').submit();
    });
    $('#group-modal').on('show.bs.modal', function() {
        $('#group-name-input').hide();
    });
    $('#group-selector-input').on('change', function() {
        if ($('#group-selector-input > select').val() == -1) {
            $('#group-name-input').show();
        } else {
            $('#group-name-input').hide();
        }
    });

    $('#gender-modal-submit-button').on('click', function() {
        $('#update-gender-form').submit();
    });
    $('#gender-modal').on('show.bs.modal', function() {
        $('#gender-other-input').hide();
    });
    $('#gender-selector-input').on('change', function() {
        if ($('#gender-selector-input > select').val() == 'other') {
            $('#gender-other-input').show();
        } else {
            $('#gender-other-input').hide();
        }
    });
});
