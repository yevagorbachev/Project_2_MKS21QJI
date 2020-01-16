//relies on jQuery being implemented on the html page
const create = function(e) {
	let form = document.getElementById('form');
	form.innerHTML = '<form action="/create" method="post">Title:<input type="text" name="name"><br>Description:<br><textarea name="description"></textarea><br><button type="submit" class="btn btn-primary">Create</button></form>';
}

document.getElementById('create').addEventListener('click', create);
