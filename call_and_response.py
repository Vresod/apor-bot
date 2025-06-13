from collections import namedtuple as _namedtuple

chanceresponse = _namedtuple('ChanceResponse', ["response", "chance"])

prompts = {
	# "call": chanceresponse(response,chance)
	# call is a regex pattern, response is a str, chance is a float 1 >= n > 0
	r"play and draw": chanceresponse("I FUCKING HATE YOU AND HOPE YOU DIE!!!!!",1),
	r"(\bhi+\b)|(\bhello+\b)": chanceresponse("bye :unamused:", 0.33),
	r"\bgoon": chanceresponse("mmm im strokin my shih rn", 0.2),
	r"\bbird\b": chanceresponse("BIRD??!?!?!", 0.2),
	"i know what you are": chanceresponse("https://i.kym-cdn.com/photos/images/original/002/357/433/996.png",1)
}