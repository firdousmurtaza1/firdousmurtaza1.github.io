$(function() {
    console.log("hi");
    $('body').on('change', ':file', function () {
        debugger
        
        var input = $(this);
        var label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        if (!label) {
            label = 'Browse File';
        }
        $('.file-upload-text', $(this).parent('label')).text(label);
    });
});