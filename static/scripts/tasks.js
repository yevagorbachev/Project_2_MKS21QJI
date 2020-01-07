//relies on jQuery being implemented on the html page

const edittask = function(e) {
	$.ajax({
		type: 'POST',
		url: '/edittask',
		data: `id=${id}&stat=${stat}&content=${content}&deadline=${deadline}`,
		success: function() {
		},
		error: function() {
		}
	});
}

const newtask = function(e) {
	$.ajax({
		type: 'POST',
		url='/newtask',
		data: `projid=${projid}`,
		success:
	})
