import os
import sys
from datetime import datetime
import gradio as gr

def save_image(image, prompt):
    # Set the output directory in your Google Drive
    output_dir = "/content/drive/MyDrive/Fooocus/output_images"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate the timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{prompt.replace(' ', '_')}_{timestamp}.png"

    # Save the image to the output directory
    image.save(os.path.join(output_dir, filename))
    return image

def update_output(output_component, image, prompt):
    output_component.update(value=save_image(image, prompt))

def entry_with_update(prompt, steps, guidance_scale, seed, width=512, height=512):
    image = pipe(prompt, num_inference_steps=steps, guidance_scale=guidance_scale, generator=torch.Generator("cuda").manual_seed(seed), width=width, height=height).images[0]
    return gr.update(visible=True), image, prompt

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root)
os.chdir(root)

try:
    import pygit2
    pygit2.option(pygit2.GIT_OPT_SET_OWNER_VALIDATION, 0)

    repo = pygit2.Repository(os.path.abspath(os.path.dirname(__file__)))

    branch_name = repo.head.shorthand

    remote_name = 'origin'
    remote = repo.remotes[remote_name]

    remote.fetch()

    local_branch_ref = f'refs/heads/{branch_name}'
    local_branch = repo.lookup_reference(local_branch_ref)

    remote_reference = f'refs/remotes/{remote_name}/{branch_name}'
    remote_commit = repo.revparse_single(remote_reference)

    merge_result, _ = repo.merge_analysis(remote_commit.id)

    if merge_result & pygit2.GIT_MERGE_ANALYSIS_UP_TO_DATE:
        print("Already up-to-date")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_FASTFORWARD:
        local_branch.set_target(remote_commit.id)
        repo.head.set_target(remote_commit.id)
        repo.checkout_tree(repo.get(remote_commit.id))
        repo.reset(local_branch.target, pygit2.GIT_RESET_HARD)
        print("Fast-forward merge")
    elif merge_result & pygit2.GIT_MERGE_ANALYSIS_NORMAL:
        print("Update failed - Did you modify any file?")
except Exception as e:
    print('Update failed.')
    print(str(e))

print('Update succeeded.')
from launch import *
