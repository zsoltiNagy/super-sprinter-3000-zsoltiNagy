from flask import render_template, request, redirect, url_for
from app import app


##################
# Global variables
##################
FIELDNAMES = ['ID',
              'Story Title',
              'User Story',
              'Acceptance Criteria',
              'Business Value',
              'Estimation',
              'Status',
              'Edit',
              'Delete']

###################################
# Functions to use for page methods
###################################


def create_dataset(file):
    '''
    Returns a 2d container from the content of the csv file.
    '''
    with open(file, "r") as csvfile:
        return [line.split('|') for line in csvfile]


def construct_line(base):
    '''
    Constructing a ready-to-write string from the form request.
    '''
    return '|'.join([base[fieldname].replace('\n', ' ').replace('\r', '') for fieldname in FIELDNAMES[1:7]])


##############
# Page methods
##############


@app.route('/story', methods=['GET', 'POST'])
def story():
    if request.method == 'POST':
        data_set = create_dataset('stories.csv')  # dataset for unique id generation
        id_ = str(int(data_set[-1][0]) + 1) + '|'  # we bind the new id to the last lines id
        values = construct_line(request.form)
        with open('stories.csv', 'a+') as csvfile:
            csvfile = csvfile.write(id_ + values + '\n')
        return redirect(url_for('list'))

    # this happens when the request method is 'GET'
    return render_template('story.html',
                           title='Add new story',
                           values=[],  # so every field of the form will be empty
                           button="Create",
                           action="/story")


@app.route('/')
@app.route('/list')
def list():
    data_set = create_dataset('stories.csv')
    return render_template("list.html", data_set=data_set, fieldnames=FIELDNAMES)


@app.route('/story/<int:story_id>', methods=['GET', 'POST'])
def get_story_by_id(story_id):
    if request.method == 'POST':
        values = construct_line(request.form)
        data_set = create_dataset('stories.csv')
        with open("stories.csv", "w") as csvfile:
            for line in data_set:
                if int(line[0]) == story_id:
                    new_line = str(story_id) + '|' + values
                    csvfile.write(new_line+'\n')
                else:
                    line = '|'.join(line)
                    csvfile.write(str(line))
        return redirect(url_for('list'))

    data_set = create_dataset('stories.csv')

    for line in data_set:
        if int(line[0]) == story_id:
            values = line
            return render_template('story.html',
                                   title='Edit Story',
                                   values=values,
                                   button="Update",
                                   action="/story/{}".format(story_id))
    return redirect(url_for('list'))


@app.route('/story/<int:story_id>/del', methods=['POST'])
def del_story_by_id(story_id):
    if request.method == 'POST':
        data_set = create_dataset('stories.csv')

        with open("stories.csv", "w") as csvfile:
            for line in data_set:
                if not int(line[0]) == story_id:
                    line = '|'.join(line)
                    csvfile.write(str(line))
        return redirect(url_for('list'))


if __name__ == '__main__':
    app.run(debug=True)
