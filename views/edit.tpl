%include header title = title
<div class="box">
	<div class="box post">
		<h2>編輯</h2>
		<form action="/save" method="post" id="post_new">
		<input type="hidden" name="id" value="{{todo.id}}" />
			<p><input type="text" name="name" value="{{todo.topic}}" class="long_txt" /></p>
			<p><input type="submit" class="submit" value="儲存" /></p>
		</form>
	</div>
</div>
%include footer title = title