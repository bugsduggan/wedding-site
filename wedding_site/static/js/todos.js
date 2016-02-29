$(function() {
    $('#add-task-modal-submit-button').on('click', function() {
        $('#add-task-form').submit();
    });

    $('#delete-task-modal').on('show.bs.modal', function(event) {
        var button = $(event.relatedTarget);
        var tid = button.data('task-tid');
        var deleteUrl = '/api/delete_task/' + tid;
        $('#delete-task-modal-delete-button').attr('href', deleteUrl);
    });
});
