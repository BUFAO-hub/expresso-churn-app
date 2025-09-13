import streamlit as st
st.title("Hello Gomycode ")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("Hello Gomycode")
st.markdown("### This is a markdown")
st.success("Success")
st.info("Information")
st.warning("Warning")
st.error("Error")
exp = ZeroDivisionError("Trying to divide by Zero")
st.exception(exp)
img = r"C:\Users\hp\OneDrive\Pictures\881643-scissor-seven-live-wallpaper-animated-wallpaper (1).jpg"
st.image(img, width=200)
if st.checkbox("Show/Hide"):

	# display the text if the checkbox returns True value
	st.text("Showing the widget")
# first argument is the title of the radio button
# second argument is the options for the radio button

status = st.radio("Select Gender: ", ('Male', 'Female'))
# conditional statement to print
# Male if male is selected else print female
# show the result using the success function

if (status == 'Male'):
	st.success("Male")
else:
	st.success("Female")
# first argument takes the titleof the selectionbox
# second argument takes options :

hobby = st.selectbox("Hobbies: ",
					['Dancing', 'Reading', 'Sports'])
# print the selected hobby :

st.write("Your hobby is: ", hobby)
hobbies = st.multiselect("Hobbies: ",
						['Dancing', 'Reading', 'Sports'])
st.write("You selected", len(hobbies), 'hobbies')
st.button("Click me for no reason")
if(st.button("About")):
	st.text("Welcome To Gomycode!!!")
name = st.text_input("Enter Your name", "Type Here ...")
if(st.button('Submit')):
	result = name.title()
	st.success(result)
# first argument takes the title of the slider
# second argument takes the starting of the slider
# last argument takes the end number
level = st.slider("Select the level", 1, 5)
# print the level
# format() is used to print value of a variable at a specific position
st.text('Selected: {}'.format(level))