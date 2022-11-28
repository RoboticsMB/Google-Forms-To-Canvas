# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 12:12:12 2021

@author: Matthew
"""

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
driver = webdriver.Chrome()
driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdXicYHlkztSFXOGxEQ6UYUfusQg4NRM236l2jwIHFRYoaOjQ/viewform?usp=pp_url')
#driver.get('https://docs.google.com/forms/d/e/1FAIpQLSelmKzC6SO9QTfHtBBw844m_4A94vuZJuhpchwUXfDfSx8xig/viewform?usp=sf_link')
def signIn():
    """
    Logs into the google form using the username(CSProject)
    and password(Python3) and an email of(CSProject@gatewayk12.net)

    Returns
    -------
    None.

    """
    email = driver.find_element_by_id("identifierId")
    email.send_keys("CSProject@gatewayk12.net")
    next_Button = driver.find_elements_by_xpath('//*[@id ="identifierNext"]') 
    next_Button[0].click()
    driver.implicitly_wait(15)
    username = driver.find_element_by_id("userNameInput")
    username.send_keys("CSProject")
    password = driver.find_element_by_id("passwordInput")
    password.send_keys("Python3")
    next_Button_Gateway = driver.find_element_by_id("submitButton")
    next_Button_Gateway.click()
    driver.implicitly_wait(15)
    continue_Button = driver.find_elements_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div') 
    continue_Button[0].click()
    

signIn()

def titleGenerator():
    """
    Gets the Title and its Description from the Google Form

    Returns
    -------
    tuple -> title = title of Form  
             title_description = description under the title

    """
    title_html = driver.find_element_by_class_name('freebirdFormviewerViewHeaderTitle ')
    title = title_html.get_attribute('innerHTML')
    title_html = driver.find_element_by_class_name('freebirdFormviewerViewHeaderDescription')
    title_description = title_html.get_attribute('innerHTML')
    return(title, title_description)

def multipleChoice_Options():
    """
    Gets all of the possible multipleChoice options

    Returns
    -------
    multiple_choice_list: list of options

    """
    #Gets all of the multiple choice bubles
    question_choices_bubble = driver.find_elements_by_class_name('docssharedWizToggleLabeledLabelText')
    multiple_choice_list = []
    #Loops over Each Choice
    for question in question_choices_bubble:
        # Gets its attribute
        current_class = question.get_attribute('class')
        # Looks for Keyword Radio
        for i in range(0,len(current_class)):
            try:
                text = current_class[i:i+5]
                if text == "Radio":
                    multiple_choice_list.append(question.get_attribute('innerHTML'))
            except:
                pass
    return multiple_choice_list

def checkbox_Options():
    """
    Gets all of the possible checkbox options

    Returns
    -------
    check_box_list : list of options

    """
    #Gets all of the multiple choice bubles
    question_choices_bubble = driver.find_elements_by_class_name('docssharedWizToggleLabeledLabelText')
    check_box_list = []
    #Loops over Each Choice
    for question in question_choices_bubble:
        current_class = question.get_attribute('class')
        # Looks for Keyword Checkbox
        for i in range(0,len(current_class)):
            try:
                text = current_class[i:i+8]
                if text == "Checkbox":
                    check_box_list.append(question.get_attribute('innerHTML'))
            except:
                pass
    return check_box_list


def dropdown_Options():
    """
    Gets all of the possible drop down options

    Returns
    -------
    dropdown_list : list of options

    """
    dropdown_list = []
    drop_down_questions = driver.find_elements_by_class_name('quantumWizMenuPaperselectContent')
    count = 0
    #loops over options excludes first one because it is a place holder
    for item in drop_down_questions:
        if count > 0:
            dropdown_list.append(item.get_attribute('innerHTML'))
        count+=1
    return dropdown_list
        




def QuestionHeadings():
    """
    Gets the Headings and Descriptions of all of the options

    Returns
    -------
    Heading_list : list of tuples
    Each tuple -> Heading = Heading of Question    descriptionList[index] = Descirption of each Heading
                  Requirement = Is it required to be answered    pointList[index] = amount of points

    """
    #Finds all Question Headings and establishes lists
    Question_Headings = driver.find_elements_by_class_name('freebirdFormviewerComponentsQuestionBaseTitle')
    Heading_list = []
    pointList = []
    index = 0
    descriptionList = []
    pointValues = driver.find_elements_by_class_name('freebirdFormviewerComponentsQuestionBaseScore')
    #Finds the Point Values of all the Questions
    for point in pointValues:
        pointList.append(point.get_attribute('innerHTML'))
    subheading = driver.find_elements_by_class_name("freebirdFormviewerComponentsQuestionBaseDescription")
    #Finds all of the subheadings of each Question
    for part in subheading:
        description = part.get_attribute("innerHTML")
        descriptionList.append(description)
    #Finds the Headings and Requirements
    for item in Question_Headings:
        #converts html of question to string uses string slicing and indexing to find Heading and Requirement
        html = str(item.get_attribute('innerHTML'))
        current_index = html.find('<span')
        Heading = ""
        Requirement = ""
        if current_index != -1:
            Heading = html[0:current_index]
        if current_index == -1:
            Heading = html[:]
            Requirement = "Non required"
        Beggining = html.find('aria-label')
        looking = html[Beggining + 12:Beggining +29]
        if looking == "Required question":
            Requirement = "Required"
        #Just in case out of bounds exception is thrown
        try:
            Heading_list.append((Heading, descriptionList[index], Requirement,pointList[index],))
            index+=1
        except:
            Heading_list.append((Heading, descriptionList[index], Requirement,0,))
    
    return Heading_list
        
def typeQuestion(html):
    """
    

    Parameters
    ----------
    html : string
        string of the html of a certain question

    Returns
    -------
    Type of Question

    """
    if html.__contains__("freebirdFormviewerComponentsQuestionRadioRoot") == True:
        return("Multiple Choice")
    if html.__contains__("freebirdFormviewerComponentsQuestionTextShort") == True:
        return("Short Answer!")
    if html.__contains__("freebirdFormviewerComponentsQuestionCheckboxChoice") == True:
        return("Checkbox!")
    if html.__contains__("freebirdFormviewerComponentsQuestionSelectSelect") == True:
        return("DropDown!")
    if html.__contains__("freebirdFormviewerComponentsQuestionTextLong") == True:
        return("Long Answer!")
    if html.__contains__("freebirdFormviewerComponentsQuestionScaleScaleRadioGroup") == True:
        return("Linear Scale!")
    if html.__contains__("freebirdFormviewerComponentsQuestionGridRowGroup") == True and html.__contains__('role="radiogroup"'):
        return("Grid Question!")
    if html.__contains__("freebirdFormviewerComponentsQuestionGridCheckboxGroup") == True:
        return("Checkbox Grid Question!")
    if html.__contains__('class="quantumWizTextinputPaperinputInputArea"><input type="date"') == True:
        return("Date Question!")
    if html.__contains__("freebirdFormviewerComponentsQuestionTimeTimeInputs"):
            return("Time Question!")
            
def typeQuestionGenerator():
    lst = []
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    for item in Each_Question:
        html = str(item.get_attribute('innerHTML'))
        if html.__contains__("freebirdFormviewerComponentsQuestionRadioRoot") == True:
            lst.append("Multiple Choice")
        if html.__contains__("freebirdFormviewerComponentsQuestionTextShort") == True:
            lst.append("Short Answer!")
        if html.__contains__("freebirdFormviewerComponentsQuestionCheckboxChoice") == True:
            lst.append("Checkbox!")
        if html.__contains__("freebirdFormviewerComponentsQuestionSelectSelect") == True:
            lst.append("DropDown!")
        if html.__contains__("freebirdFormviewerComponentsQuestionTextLong") == True:
            lst.append("Long Answer!")
        if html.__contains__("freebirdFormviewerComponentsQuestionScaleScaleRadioGroup") == True:
            lst.append("Linear Scale!")
        if html.__contains__("freebirdFormviewerComponentsQuestionGridRowGroup") == True and html.__contains__('role="radiogroup"'):
            lst.append("Grid Question!")
        if html.__contains__("freebirdFormviewerComponentsQuestionGridCheckboxGroup") == True:
            lst.append("Checkbox Grid Question!")
        if html.__contains__('class="quantumWizTextinputPaperinputInputArea"><input type="date"') == True:
            lst.append("Date Question!")
        if html.__contains__("freebirdFormviewerComponentsQuestionTimeTimeInputs"):
            lst.append("Time Question!")
    return lst      

def multiplechoiceCrossReference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    outsideValue = 0
    order = 1
    choices = []
    finalList = []
    for item in Each_Question:
        choices = []
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "Multiple Choice":
            options = multipleChoice_Options()
            value = outsideValue
            html = str(item.get_attribute('innerHTML'))
            for opt in options:
                index_start = html.find('data-value=')
                index_finish = html.find('role="radio"')
                try:
                    Choice = html[index_start + 12: index_finish - 2]
                except:
                    break
                try:
                    reference = multipleChoice_Options()[value]
                except:
                    break
                try:
                    if Choice == reference:
                        choices.append(reference)
                        html = html[index_finish + 13:]
                        value+=1
                    elif Choice == "__other_option__" and reference == "Other:":
                        choices.append(reference)
                        value+=1
                        outsideValue = value
                        finalList.append((choices, order,))
                        order+=1
                        choices = []
                        html = html[index_finish + 13:]
                        break
                    else:
                        outsideValue = value
                        finalList.append((choices, order,))
                        order+=1
                        choices = []
                        break
                except:
                    break
    return finalList


def checkBoxCrossReference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    outsideValue = 0
    order = 1
    choices = []
    finalList = []
    for item in Each_Question:
        choices = []
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "Checkbox!":
            options = checkbox_Options()
            value = outsideValue
            html = str(item.get_attribute('innerHTML'))
            for opt in options:
                index_start = html.find('data-answer-value')
                index_finish = html.find('role="checkbox"')
                try:
                    Choice = html[index_start + 19: index_finish - 2]
                except:
                    break
                try:
                    reference = checkbox_Options()[value]
                except:
                    break
                if Choice != reference:
                   Choice = html[(index_start+19): (index_start + 35)]
                try:
                    if Choice == reference:
                        choices.append(reference)
                        html = html[index_finish + 16:]
                        value+=1
                    elif Choice == "__other_option__" and reference == "Other:":
                        choices.append(reference)
                        value+=1
                        outsideValue = value
                        finalList.append((choices, order,))
                        order+=1
                        choices = []
                        html = html[index_finish + 16:]
                        break
                    else:
                        outsideValue = value
                        finalList.append((choices, order,))
                        order+=1
                        choices = []
                        break
                except:
                    break
    return finalList

def dropDownCrossReference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    outsideValue = 0
    order = 0
    choices = []
    finalList = []
    for item in Each_Question:
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "DropDown!":
            choices = []
            options = dropdown_Options()
            value = outsideValue
            html = str(item.get_attribute('innerHTML'))
            before = html.find('data-value=')
            html = html[before+13:]
            flag = False
            for opt in options:
                index_start = html.find('data-value=')
                index_finish = html.find('aria-selected="false" role="option"')
                try:
                    Choice = html[index_start + 12: index_finish - 2]
                except:
                    break
                try:
                    reference = dropdown_Options()[value]
                except:
                    break
                try:
                    if Choice == reference:
                        choices.append(reference)
                        value+=1
                        outsideValue = value
                        html = html[index_finish + 13:]
                    else:
                        flag = True
                        outsideValue = value
                        finalList.append((choices, order,))
                        order+=1
                        choices = []
                        break
                except:
                    flag = True
                    outsideValue = value
                    finalList.append((choices, order,))
                    order+=1
                    choices = []
                    break
    if flag == False:
        finalList.append((choices, order,))
    return finalList

def Linear_Options_Reference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    order = 0
    finalList = []
    HeadingChoices = []
    choices = []
    for item in Each_Question:
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "Linear Scale!":
            html = str(item.get_attribute('innerHTML'))
            while True:
                try:
                    index_start = html.find('data-value="')
                    index_finish = html.find('" role="radio"')
                    if (index_start == -1 or index_finish == -1):
                        break
                    Choice = html[index_start + 12: index_finish]
                    choices.append(Choice)
                    html = html[index_finish + 15:]
                except:
                    break
            html = str(item.get_attribute('innerHTML'))
            while True:
                try:
                    index_start = html.find('class="freebirdMaterialScalecontentRangeLabel">')
                    temp = html[index_start + 47:]
                    index_finish = temp.find('</div>')
                    if (index_start == -1 or index_finish == -1):
                        break
                    Heading = html[index_start + 47:index_start + 47 +index_finish]
                    HeadingChoices.append(Heading)
                    html = html[index_start + 47 +index_finish:]
                except:
                    break
                    
            finalList.append((HeadingChoices, choices, order,))
            order += 1
    return finalList
                

def grid_Question_Reference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    all_Columns = []
    all_Rows = []
    finalList = []
    order = 0
    for item in Each_Question:
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "Grid Question!":
            html = str(item.get_attribute('innerHTML'))
            #print(html)
            while True:
                try:
                    index_start = html.find('<div class="freebirdFormviewerComponentsQuestionGridCell">')
                    temp = html[index_start + 58:]
                    index_finish = temp.find('</div>')
                    if (index_start == -1 or index_finish == -1):
                        break
                    column = html[index_start+58:index_start+58+index_finish]
                    all_Columns.append(column)
                    html = html[index_start+58+index_finish:]
                    if html[0:12] == "</div></div>":
                        break
                except:
                    break
            
            html = str(item.get_attribute('innerHTML'))
            while True:
                try:
                    index_start = html.find('class="freebirdFormviewerComponentsQuestionGridCell freebirdFormviewerComponentsQuestionGridRowHeader">')
                    temp = html[index_start + 103:]
                    index_finish = temp.find('</div>')
                    if (index_start == -1 or index_finish == -1):
                        break
                    row = html[index_start+103:index_start+103+index_finish]
                    all_Rows.append(row)
                    html = html[index_start+103+index_finish:]
                except:
                    break
    half = int(len(all_Rows)/2)
    all_Rows = all_Rows[1:half]
    finalList.append((all_Rows, all_Columns,order,))
    order + 1
    return finalList
                    
def gridCheckbox_Question_Reference():
    Each_Question = driver.find_elements_by_class_name('freebirdFormviewerViewNumberedItemContainer')
    all_Columns = []
    all_Rows = []
    finalList = []
    order = 0
    for item in Each_Question:
        html = str(item.get_attribute('innerHTML'))
        typpe = typeQuestion(html)
        if typpe == "Checkbox Grid Question!":
            html = str(item.get_attribute('innerHTML'))
            while True:
                try:
                    index_start = html.find('<div class="freebirdFormviewerComponentsQuestionGridCell">')
                    temp = html[index_start + 58:]
                    index_finish = temp.find('</div>')
                    if (index_start == -1 or index_finish == -1):
                        break
                    column = html[index_start+58:index_start+58+index_finish]
                    all_Columns.append(column)
                    html = html[index_start+58+index_finish:]
                    if html[0:12] == "</div></div>":
                        break
                except:
                    break
            
            html = str(item.get_attribute('innerHTML'))
            while True:
                try:
                    index_start = html.find('class="freebirdFormviewerComponentsQuestionGridCell freebirdFormviewerComponentsQuestionGridRowHeader">')
                    temp = html[index_start + 103:]
                    index_finish = temp.find('</div>')
                    if (index_start == -1 or index_finish == -1):
                        break
                    row = html[index_start+103:index_start+103+index_finish]
                    all_Rows.append(row)
                    html = html[index_start+103+index_finish:]
                except:
                    break
    half = int(len(all_Rows)/2)
    all_Rows = all_Rows[1:half]
    finalList.append((all_Rows, all_Columns,order,))
    order + 1
    return finalList


def Complete_Question_Information_Generator():
    """
    Combines all of the data from previous functions
    """
    completeData = []
    
    Headings = QuestionHeadings()
    types = typeQuestionGenerator()
    numberOfMultipleChoice = multiplechoiceCrossReference()
    numberOfCheckBoxs = checkBoxCrossReference()
    numberOfDropDowns = dropDownCrossReference()
    numberOfLinearScales = Linear_Options_Reference()
    numberOfGridQuestions = grid_Question_Reference()
    numberOfCheckBoxGridQuestions = gridCheckbox_Question_Reference()
    for i in range(0,len(Headings)):
        if types[i] == "Multiple Choice":
            completeData.append((types[i], Headings[i], numberOfMultipleChoice[0],))
            del numberOfMultipleChoice[0]
        if types[i] == "Short Answer!":
            completeData.append((types[i], Headings[i],))
        if types[i] == "Checkbox!":
            completeData.append((types[i], Headings[i], numberOfCheckBoxs[0],))
            del numberOfCheckBoxs[0]
        if types[i] == "DropDown!":
            completeData.append((types[i], Headings[i], numberOfDropDowns[0],))
            del numberOfDropDowns[0]
        if types[i] == "Long Answer!":
            completeData.append((types[i], Headings[i],))
        if types[i] == "Linear Scale!":
            completeData.append((types[i], Headings[i], numberOfLinearScales[0],))
            del numberOfLinearScales[0]
        if types[i] == "Grid Question!":
            completeData.append((types[i], Headings[i], numberOfGridQuestions[0],))
            del numberOfGridQuestions[0]
        if types[i] == "Checkbox Grid Question!":
            completeData.append((types[i], Headings[i], numberOfCheckBoxGridQuestions[0],))
            del numberOfCheckBoxGridQuestions[0]
        if types[i] == "Date Question!":
            completeData.append((types[i], Headings[i],))
        if types[i] == "Time Question!":
            completeData.append((types[i], Headings[i],))
    return completeData



driverC = webdriver.Chrome()
driverC.get("https://adfs.gatewayk12.org/adfs/ls/?SAMLRequest=fVLLTuMwFN0jzT9Y3ucJQshqgjogNJV4RDTMYnauc%2Bt4xo%2Fg6zTw97gpCFhMt8fnnsf1XVy%2BGE124FE5W9EizSkBK1ynrKzoU3uTXNDL%2BsfJArnRA1uOobeP8DwCBhInLbL5oaKjt8xxVMgsN4AsCLZe3t2yMs3Z4F1wwmlKVtcV7bXRW7Uxfb%2Bxuu8E9E7%2B5VJwyXlEN5qDBBgMJb8%2FYpX7WCvEEVYWA7chQnlZJPlpcpq3ZcnOzlle%2FKGkeXf6qeyhwbFYmwMJ2a%2B2bZLmYd3OAjvVgb%2BP7IpK56SGVDizt284otpFeMs1AiVLRPAhBrxyFkcDfg1%2BpwQ8Pd7GliEMyLJsmqb0UybjmeQBJv76ryhT52XGBdJ63i6bC%2Fovaz0en3%2FY0%2FqIwSL7ol2%2Ff%2BO%2B3eq6cVqJV7LU2k1XHuJYRYMfY7Mb5w0P%2F7cv0mJGVJdsZyobLQ4g1FZBR0lWH1y%2F30u8ojc%3D&RelayState=https%3A%2F%2Faccounts.google.com%2FCheckCookie%3Fcontinue%3Dhttps%253A%252F%252Faccounts.google.com%252Fo%252Fsaml2%252Finitsso%253Fidpid%253DC0475tf8j%2526spid%253D108734373199%2526forceauthn%253Dfalse%2526hd%253Dgatewayk12.org%2526from_login%253D1%2526as%253DITkzH9TZRhcSilaF_PO8wyvlmGWMGYREtyYISn2Wfk4%26scc%3D1%26oauth%3D1%26ltmpl%3Dpopup")

def Canvas_SignIn():
    """
    Signs into Canvas
    """
    username = driverC.find_element_by_id("userNameInput")
    username.send_keys("CSProject")
    password = driverC.find_element_by_id("passwordInput")
    password.send_keys("Python3")
    next_Button_Gateway = driverC.find_element_by_id("submitButton")
    next_Button_Gateway.click()
    driverC.implicitly_wait(15)
    continue_Button = driverC.find_elements_by_xpath('//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div') 
    continue_Button[0].click()
    course_selection = driverC.find_element_by_class_name("ic-DashboardCard__header_content")
    course_selection.click()
    quizzes = driverC.find_element_by_class_name("quizzes")
    quizzes.click()
    Part1 = driverC.find_elements_by_tag_name("button")
    Part2 = driverC.find_elements_by_class_name("btn")
    for element in Part1:
        for clas in Part2:
            if element == clas:
                index = Part1.index(element)
                Part1[index].click()
    
Canvas_SignIn()

def QuizBuild():
    """
    Builds the Quiz based on Previous Data

    Returns
    -------
    None.

    """
    #Makes Quiz Name and Description
    driverC.implicitly_wait(15)
    Quiz_Title = driverC.find_element_by_id("quiz_title")
    Quiz_Title.clear()
    Quiz_Title.send_keys(titleGenerator()[0])
    driverC.switch_to_frame(1)
    Quiz_Description = driverC.find_element_by_id('tinymce')
    Quiz_Description.send_keys(titleGenerator()[0])
    driverC.switch_to_default_content()
    QuestionTab = driverC.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/ul/li[2]/a")
    QuestionTab.click()

    data = Complete_Question_Information_Generator()
    #Loops over the data provided and creates a quiz
    for i in range(0,len(data)):
        NewQuestion = driverC.find_element_by_xpath('//*[@id="questions_tab"]/div[15]/a[1]')
        NewQuestion.click()
        part = data[i]
        description = part[1]
        QuestionName = driverC.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/div[2]/div[2]/div/form/div/div[1]/input[1]')
        QuestionName.send_keys(str(description[0]))    
        Type = driverC.find_element_by_name('question_type')
        Type.click()
        driverC.switch_to_frame(2)
        Question_Description = driverC.find_element_by_id('tinymce')
        Question_Description.send_keys(str(description[0]))
        Question_Description.send_keys(Keys.ENTER)
        Question_Description.send_keys(str(description[1]))
        driverC.switch_to_default_content()
        options = driverC.find_elements_by_tag_name('option')
        choices = options[8:20]
        Chosen = part[0]
        Adjusted = "Multiple Choice"
        if Chosen == 'Short Answer!':
            Adjusted = "Essay Question"
        if Chosen == 'Checkbox!':
            Adjusted = 'Multiple Answers'
        if Chosen == 'DropDown!':
            Adjusted = 'Multiple Choice'
        if Chosen == "Long Answer!":
            Adjusted = "Essay Question"
        if Chosen == "Linear Scale!":
            Adjusted = "Multiple Choice"
        if Chosen == "Grid Question!":
            Adjusted = 'Matching'
        if Chosen == "Checkbox Grid Question!":
            Adjusted = 'Matching'
        if Chosen == "Date Question!":
            Adjusted = "Essay Question"
        if Chosen == "Time Question!":
            Adjusted = "Essay Question"
        for option in choices:
            if option.get_attribute('innerHTML') == Adjusted:
                option.click()
                break
        if Chosen == "Multiple Choice" or Chosen == "DropDown!" or Chosen == "Checkbox!":
            possibleAnswers = part[2]
            possibleAnswers = possibleAnswers[0]
            amountClick = 0
            count = 0
            Name = driverC.find_elements_by_name('answer_text')
            Class = driverC.find_elements_by_class_name('disabled_answer')
            for e in Name:
                for c in Class:
                    if e == c:
                        count +=1
                
            count -= 1
            if len(possibleAnswers) > 2 and count != 4:
                amountClick = len(possibleAnswers) - 2
            AnotherAdd = driverC.find_elements_by_class_name('add_answer_link')
            for i in range(0,amountClick):
                AnotherAdd[0].click()
            num = 1
            for i in range(0,len(possibleAnswers)):
                xpath = '/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/div[2]/div[2]/div/form/div/div[4]/div[27]/div[]/table/tbody/tr[1]/td[2]/div[1]/input[1]'
                #complete = xpath[0:114]+str(num)+xpath[114+len(str(num))-1:len(xpath)+len(str(num))]
                complete = xpath[0:114]+str(num)+xpath[114+len(str(num))-len(str(num)):len(xpath)+len(str(num))]
                Answer = driverC.find_element_by_xpath(complete)
                Answer.send_keys(possibleAnswers[i])
                num+=1
            point = driverC.find_element_by_name('question_points')
            point.clear()
            point.send_keys(description[3])
        
        if Chosen == "Linear Scale!":
            startingpoints = part[2][0]
            driverC.switch_to_frame(2)
            LinearDescription = driverC.find_element_by_id('tinymce')
            LinearDescription.send_keys(Keys.ENTER)
            directions = startingpoints[0]+' to '+startingpoints[1]
            LinearDescription.send_keys(directions)
            driverC.switch_to_default_content()
            possibleAnswers = part[2][1]
            amountClick = 0
            if len(possibleAnswers) > 2:
                amountClick = len(possibleAnswers) - 2
            AnotherAdd = driverC.find_elements_by_class_name('add_answer_link')
            for i in range(0,amountClick):
                AnotherAdd[0].click()
            num = 1
            for i in range(0,len(possibleAnswers)):
                xpath = '/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/div[2]/div[2]/div/form/div/div[4]/div[27]/div[]/table/tbody/tr[1]/td[2]/div[1]/input[1]'
                complete = xpath[0:114]+str(num)+xpath[114+len(str(num))-len(str(num)):len(xpath)+len(str(num))]
                Answer = driverC.find_element_by_xpath(complete)
                Answer.send_keys(possibleAnswers[i])
                num+=1
            point = driverC.find_element_by_name('question_points')
            point.clear()
            point.send_keys(description[3])
        driverC.implicitly_wait(15)
        
        if Chosen == "Grid Question!":
            place = driverC.find_element_by_name('matching_answer_incorrect_matches')
            columns = part[2][1]
            for choice in columns:
                place.send_keys(choice)
                place.send_keys(Keys.ENTER)
            
            rows = part[2][0]
            amountClick = 0
            if len(rows) > 4:
                amountClick = len(rows) - 4
            AnotherAdd = driverC.find_elements_by_class_name('add_answer_link')
            for i in range(0,amountClick):
                AnotherAdd[0].click()
            num = 1
            for i in range(0, len(rows)):
                xpath = '/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/div[2]/div[2]/div[7]/form/div/div[4]/div[27]/div[]/table/tbody/tr[1]/td[2]/div[4]/div[1]/input'
                complete = xpath[0:117]+str(num)+xpath[117+len(str(num))-len(str(num)):len(xpath)+len(str(num))]
                Answer = driverC.find_element_by_xpath(complete)
                Answer.send_keys(rows[i])
                num+=1
            point = driverC.find_element_by_name('question_points')
            point.clear()
            point.send_keys(description[3])
            
        if Chosen == "Checkbox Grid Question!":
            place = driverC.find_element_by_name('matching_answer_incorrect_matches')
            columns = part[2][1]
            for choice in columns:
                place.send_keys(choice)
                place.send_keys(Keys.ENTER)
            
            rows = part[2][0]
            amountClick = 0
            if len(rows) > 4:
                amountClick = len(rows) - 4
            AnotherAdd = driverC.find_elements_by_class_name('add_answer_link')
            for i in range(0,amountClick):
                AnotherAdd[0].click()
            num = 1
            for i in range(0, len(rows)):
                xpath = '/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/div/div[1]/div/div[3]/div[2]/div[2]/div[8]/form/div/div[4]/div[27]/div[]/table/tbody/tr[1]/td[2]/div[4]/div[1]/input'
                complete = xpath[0:117]+str(num)+xpath[117+len(str(num))-len(str(num)):len(xpath)+len(str(num))]
                Answer = driverC.find_element_by_xpath(complete)
                Answer.send_keys(rows[i])
                num+=1
            point = driverC.find_element_by_name('question_points')
            point.clear()
            point.send_keys(description[3])
           
        point = driverC.find_element_by_name('question_points')
        point.clear()
        point.send_keys(description[3])
        
QuizBuild()
    
    
    
    
    
