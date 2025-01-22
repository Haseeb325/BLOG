
from django.shortcuts import render
from django.shortcuts import HttpResponse , redirect
from .models import Post , BlogComment

from django.contrib import messages
from blog.templatetags import extras

# Create your views here.

def blogHome (request):
    allPosts = Post.objects.all()
    # print(allPosts)
    context ={'allPosts':allPosts}

    return render (request , 'blog/blogHome.html' , context)
    # return HttpResponse("HEY BLOGHOME")

def blogPost(request , slug):
    # post  = Post.objects.filter(slug = slug)[0] 
    post  = Post.objects.filter(slug = slug).first()
    # post  = Post.objects.get(slug = slug)
    # ye comments wala kam baad mai kia jb postComment wala function banaya

    comments = BlogComment.objects.filter(post = post , parent =None) #parent None krne ki waja se dirf direct wale comment nzr ayen ge baqi sub replies nhi dikhen ge 
    replies = BlogComment.objects.filter(post = post).exclude(parent =None) # jin ka parent None Nahi hoga wo comments milen gay .exclude mtlb != ya !None ye notations directly nahi lga skte is liay .exclude lagaya
    # print("comments " , comments)
    # print("replies" , replies)
    # for i in comments :
    #     print("comment",i)
  
    replyDict = {}
    # hr reply ko alg alg kr k objects mtlb list [] bna k dictionary mai add kr dia
    for reply in replies:    
        if reply.parent.sno not in replyDict.keys():
        #  idhr sno k according reply ko sno k equal kre ga 
         replyDict[reply.parent.sno] = [reply]
        else:
            # idhr [] is trah alg alg objects bn k dictionary {} mai add ho jayn gay 
            replyDict[reply.parent.sno].append(reply)

# wese ye b thk hai ye b work kre ga
    # replyDict = {}
    # # hr reply ko alg alg kr k dictionary bna di
    # for reply in replies:    
    #     if reply.sno not in replyDict.keys():
    #      replyDict[reply.sno] = [reply] 

    # print(reply.parent.sno,replyDict)

    # filter use krne se queryset milta hai [<Post:hmmby fateh] is trah phr is ko lene k liay [0] lagana prta hai taake fetch ho ske lekin [0] nhi lagana to phr .first b lga skte  
    #  jb k get se direct object mil jata hai aese hmmbyfateh
    # print(post)
    print(request.user)
    context ={ "post":post ,
               "comments":comments ,
                "user" :request.user,
                "replyDict" : replyDict
                 }
    return render (request , 'blog/blogPost.html' , context)
    # return HttpResponse (f"HEY BLOG {slug}")


# def postComment(request):


#     if request.method == "POST":

#         comment =  request.POST.get("comment")
#         # print("comment" , comment)
#         user = request.user
#         print(user)
#         postSno = request.POST.get("postSno")
#         print(postSno)
#         post =  Post.objects.get(sno=postSno)
#         print(post)

#         # comment= BlogComment(comment=comment ,user =user , post = post )
#         # comment.save()
       
#         # messages.success(request , "Your comment has been posted successfully")
#         print( "comments",comment)
        
 
#         return redirect(f"/blog/{post.slug}/")


# def postComment(request):
#     if request.method == "POST":
#         comment_text = request.POST.get('comment')
#         post_sno = request.POST.get('postSno')
#         post = Post.objects.get(sno=post_sno)
#         user = request.user

#         # Save the comment in the database
#         comment = BlogComment(comment=comment_text, user=user, post=post)
#         comment.save()

#         # Optionally, add a success message
#         messages.success(request, "Your comment has been posted successfully!")

#         # Redirect to the same blog post page to show the comment
#         return redirect('blogPost', slug=post.slug)


# # # Views.py
# def postComment(request):
#     if request.method == "POST":
#         comment = request.POST.get("comment")
#         postSno = request.POST.get("postSno")

#         # Debugging
#         print("Comment:", comment)
#         print("Post ID (Sno):", postSno)

#         if not comment.strip():  # More robust check for empty comments
#             messages.error(request, "Comment cannot be empty.")
#             return redirect(f"/blog/{postSno}")

#         try:
#             post = Post.objects.get(sno=postSno)
#         except Post.DoesNotExist:
#             messages.error(request, "Post not found.")
#             return redirect("/blog/")

#         user = request.user
#         blog_comment = BlogComment(comment=comment, user=user, post=post)
#         blog_comment.save()

#         messages.success(request, "Your comment has been posted successfully.")

#         return redirect(f"/blog/{post.slug}")

#     return redirect("/")





def postComment(request):
    if request.method == "POST":
        # Get the comment and postSno from the form
        comment = request.POST.get("comment")
        postSno = request.POST.get("postSno")  
        parentSno = request.POST.get("parentSno")

        print("postSno",postSno)
        print("parentSno",parentSno)


        # Debugging
        print("Comment:", comment)
        print("Post ID (Sno):", postSno)

        # Ensure comment is not empty
        if not comment:
            messages.error(request, "Comment cannot be empty.")
            return redirect(f"/blog/{postSno}")

        # Get the post object
        try:
            post = Post.objects.get(sno=postSno)
        except Post.DoesNotExist:
            messages.error(request, "Post not found.")
            return redirect("/blog/")  # Redirect to the blog page

        # Get the logged-in user
        user = request.user

        # Create and save the comment
        if parentSno == "":
            blog_comment = BlogComment(comment=comment, user=user, post=post)
            blog_comment.save()
            messages.success(request, "Your comment has been posted successfully.")

        else:
                parent = BlogComment.objects.get(sno = parentSno)
                blog_comment = BlogComment(comment=comment, user=user, post=post , parent = parent )
                blog_comment.save()

        # Success message
                messages.success(request, "Your reply has been posted successfully.")

        # Debugging
        print("Saved Comment:", blog_comment)

        # Redirect back to the post page
        return redirect(f"/blog/{post.slug}")

    # If not a POST request, redirect to the post page
    return redirect("/")