from django import forms


TEST_NUMBER = [
	('1', '1'),
	('2', '2'),
	('3', '3'),
]

labs = [
	('Medichecks', 'Medichecks'),
	('EMC', 'EMC'),
	('FML ME', 'FML ME'),
	('Lenco','Lenco'),
	('TDL','TDL'),
	('Invitro','Invitro'),
	('Medsi / Chromolab', 'Medsi / Chromolab'),
	('Medical Diagnosis','Medical Diagnosis'),
	('Chromolab / KDL', 'Chromolab / KDL'),
	('All', 'All'),
	]



components = [
	('Vitamine Komplex', 'Vitamine Komplex'),
	('Spurenelemente SE Komplex', 'Spurenelemente SE Komplex'),
	('Coenzym Q10 retard','Coenzym Q10 retard'),
	('Chrom [Chromium]', 'Chrom [Chromium]'),
	('Eisen [Iron]', 'Eisen [Iron]'),
	('Folsäure [Folic acid]', 'Folsäure [Folic acid]'),
	('Glutathion', 'Glutathion'),
	('Inositol Hexanicotinat', 'Inositol Hexanicotinat'),
	('Isoflavone Extrakt', 'Isoflavone Extrakt'),
	('Glutamin (L-)', 'Glutamin (L-)'),
	('Griffonia simplicifolia [L-5-HTP]', 'Griffonia simplicifolia [L-5-HTP]'),
	('Lysin (L-)', 'Lysin (L-)'),
	('Tryptophan (L-)', 'Tryptophan (L-)'),
	('Rhodiola Extrakt', 'Rhodiola Extrakt'),
	('Selen [Selenium]', 'Selen [Selenium]'),
	('Silymarin Extrakt', 'Silymarin Extrakt'),
	('Vitamin B1', 'Vitamin B1'),
	('Vitamin B6', 'Vitamin B1'),
	('Vitamin B12', 'Vitamin B12'),
	('Vitamin C', 'Vitamin C'),
	('Vitamin D3', 'Vitamin D3'),
	('Vitamin K2', 'Vitamin K2'),
	("Vitamin E NAT Komplex","Vitamin E NAT Komplex"),
	("Zink","Zink"),
	("Tyrosin (L-)","Tyrosin (L-)"),
	("Liponsäure (α-) [Lipoic acid]","Liponsäure (α-) [Lipoic acid]"),
	("Bioflavonoide Komplex","Bioflavonoide Komplex"),
	("Biotin","Biotin"),
	("Curcumin und Piperin","Curcumin und Piperin"),
	("Ginseng Extrakt","Ginseng Extrakt"),
	("Glucosaminsulfat","Glucosaminsulfat"),
	("Kupfer [Copper]","Kupfer [Copper]"),
	("Lycopen","Lycopen"),
	("Methylsulfonylmethan (MSM)","Methylsulfonylmethan (MSM)"),
	("Chondroitinsulfat [Chondroitin sulphate]","Chondroitinsulfat [Chondroitin sulphate]"),
	("OPC Grape Seed","OPC Grape Seed"),
	("Leucin (L-)","Leucin (L-)"),
	("Isoleucin (L-)","Isoleucin (L-)"),
	("Ginkgo Extrakt","Ginkgo Extrakt"),
	("Kreatin","Kreatin"),
	("Carnosin (L-)","Carnosin (L-)"),
	("Glycin","Glycin"),
	("Selenhefe [Selenium yeast]","Selenhefe [Selenium yeast]"),
	("Magnesium","Magnesium"),
	("Kalium [Potassium]","Kalium [Potassium]"),
	("Calcium L-(+)-Lactat Komplex","Calcium L-(+)-Lactat Komplex"),
	("Taurin","Taurin"),
	("Arginin (L-)","Arginin (L-)"),
	("Carnitin (L-)","Carnitin (L-)"),
	("Aminomix NAC","Aminomix NAC"),
	("Aroma Orange [Flavour orange]","Aroma Orange [Flavour orange]"),
	("Antioxidantien [Antioxidants]", "Antioxidantien [Antioxidants]"),
	]




class LocationForm(forms.Form):
	
	order_number = forms.ChoiceField(choices=TEST_NUMBER)
	lab = forms.ChoiceField(choices=labs)
	component=forms.ChoiceField(choices=components)



TEST_NUMBER = [
	('1', '1'),
	('2', '2'),
	('3', '3'),
]

class OrderForm(forms.Form):
	order_number = forms.ChoiceField(choices=TEST_NUMBER)

normaltests = [
	('Vitamin D', 'Vitamin D'),
	('Vitamin B9 (Folic acid)', 'Vitamin B9 (Folic acid)'),
	('Triglycerides', 'Triglycerides'),
	('Creatinine', 'Creatinine'),
	('AST', 'AST'),
	('ALT', 'ALT'),
	('Uric acid', 'Uric acid'),
	('Total cholesterol', 'Total cholesterol'),
	('Homocysteine', 'Homocysteine'),
	('Copper', 'Copper')
]

class TestForm(forms.Form):
	tests = forms.ChoiceField(choices=normaltests)

byposi = [
	('by result position', 'by result position'),
	('by panel position', 'by panel position'),
	('by normal position', 'by normal position'),
]

class ByPosForm(forms.Form):
	bypos = forms.ChoiceField(choices=byposi)

class Loading(forms.Form):
	answer = forms.IntegerField()
