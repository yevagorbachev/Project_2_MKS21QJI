//relies on jQuery being implemented on the html page

const edittask = function(e) {
	let id = this.id;
	let stat = document.getElementById("status").value;
	let content = document.getElementById("content").value;
	let deadline = document.getElementById("deadline").value;
	$.ajax({
		type: 'POST',
		url: '/edittask',
		data: `id=${id}&stat=${stat}&content=${content}&deadline=${deadline}`,
		success: function(html) {
			let task = document.getElementById(`${id}`);
			task.innerHTML = html;
		},
		error: function(err) {
			console.log(err);
		}
	});
};

const newtask = function(e) {
	let projid = document.getElementById("projid").value;
	$.ajax({
		type: 'POST',
		url='/newtask',
		data: `projid=${projid}`,
		success: function(id) {
			let task = document.createElement("div");
			task.id = id;
			task.addEventListener("click", edittask);
			document.getElementById("tasks").appendChild(task);
			edittask(task);
		}
		error: function(err) {
			console.log(`could not create new element: ${err}`);
		}
	});
};

var tasks = document.getElementsByTagName("div");
for(var i = 0; i < tasks.length; i++) {
	tasks[i].addEventListener("click", edittask);
}
document.getElementById("create").addEventListener("click", newtask);
