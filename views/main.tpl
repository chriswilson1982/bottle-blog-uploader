<!DOCTYPE html>
<html lang="en">

  <head>

    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="Church View Medical Practice">
    <meta name="author" content="Church View Medical Practice">

    <title>App | Church View Medical Practice</title>

    <!-- Bootstrap core CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <!-- Font Awesome CSS -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/css/main.css">

    <!-- JQuery -->
    <script src="https://code.jquery.com/jquery-3.4.1.js" integrity="sha256-WpOohJOqMqqyKL9FccASB9O0KwACQJpFTUBLTYOVvVU=" crossorigin="anonymous"></script>

    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
    <!-- Custom JS -->
    <script src="/js/main.js"></script>

  </head>

  <body>
  
  % include('header.tpl')

    <div class="container my-4">

      <div class="row">

        <!-- Form column -->
        <div class="col-md-7 py-5">

          <h1>Submit Article</h1>
          
          <h2 class="mt-4 mb-3" id="subtitle">News</h2>

          <!-- Form -->
          <form id="update-form" method="POST" enctype="multipart/form-data" accept-charset="utf-8">

            <!-- Type -->
            <div class="form-group">
              <label class="col-form-label bold" for="type"><h5 class="mb-0">Type</h5></label>
              <select class="form-control" name="type" id="type">
                <option value="0">News</option>
                <option value="1">Health Blog</option>
              </select>
            </div>

            <!-- Title -->
            <div class="form-group mt-3">
              <label class="col-form-label bold" for="title"><h5 class="mb-0">Title</h5></label>
              <input class="form-control" type="text" name="title" id="title" placeholder="Title" required/>
            </div>

            <!-- Body -->
            <div class="form-group mt-3">
              <label class="col-form-label bold" for="body"><h5 class="mb-0">Main Text</h5></label>
              <textarea class="form-control" name="body" id="body" placeholder="Main text" rows=12 required></textarea>
            </div>
            <!-- Button group -->
            <div class="mb-4">
            <button class="btn btn-secondary" onclick="insertHeaderTag();">Heading</button>
            <button class="btn btn-secondary" onclick="insertImageTag();">Image</button>
            <button class="btn btn-secondary" onclick="insertLinkTag();">Link</button>
            <button class="btn btn-secondary" onclick="insertGPOOHinfo();">GP OOH</button>
            </div>

            <!-- Image -->
            <div class="form-group mt-3">
              <label class="col-form-label bold" for="file"><h5 class="mb-1">Image Upload</h5></label>
              <input class="d-block" type="file" name="file" id="file" />
              <label class="form-label mt-1 text-muted"><small>Optional. Images should be JPEG or PNG format and will be resized and cropped to 700x400 pixels if necessary.</small></label>
            </div>
            
            <!-- Author -->
            <div class="form-group mt-3">
              <label class="col-form-label bold" for="author"><h5 class="mb-0">Author</h5></label>
              <select class="form-control" name="author" id="author">
                <option value="Church View Medical Practice">Church View Medical Practice</option>
                <option value="Dr Ruth Doggart">Dr Ruth Doggart</option>
                <option value="Dr Fiona Hunter">Dr Fiona Hunter</option>
                <option value="Dr Stephen Maconachie">Dr Stephen Maconachie</option>
                <option value="Mrs Paula Skillen">Mrs Paula Skillen</option>
                <option value="Dr Chris Wilson">Dr Chris Wilson</option>
                
              </select>
            </div>
            
            <!-- Publish -->
            <div class="form-group my-5"><label class="mb-0 bold" for="publish"><h5>Publish Now</h5></label><input class="mx-3 mb-0" type="checkbox" name="publish" id="publish" checked /><i id="publish-indicator" class="mb-0 fas fa-circle text-success"></i>
            <label class="form-label my-0 text-muted"><small>Select to publish article immediately. Unpublished articles will be saved and can be published later.</small></label>
            </div>

            <!-- Password -->
            <div class="form-group mt-5">
              <label class="col-form-label bold" for="password"><h5 class="mb-0">Password</h5></label>
              <input class="form-control" type="password" name="password" id="password" placeholder="Password" required>
            </div>

            <!-- Button -->
            <input id="submit-button" class="btn btn-primary w-100 mt-3" type="submit" value="Submit Article">
            
            

          </form>

        </div> <!-- /.col -->

        <!-- Library column -->
        <div id="previous-articles" class="col-md-5 py-5">

          <h1>Previous articles</h1>

        </div> <!-- /.col -->

      </div> <!-- /.row -->

    </div> <!-- ./container -->

    

  </body> <!-- /body -->

</html>
