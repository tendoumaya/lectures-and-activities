T = "The peaks with the largest 2θ value might be related to the Au on the surface, for the integral area shows a positive correlation to Au presented. The peaks with 2θ about 62 remain roughly identical, which might be strongly related to Si substrate or other elements with an irregular structure or trace amount."
L=10
function Generate_Brief(text, length) {
    if (text.length < length) return text;
    var Foremost = text.substr(0, length);
    var re = /<(\/?)(BODY|SCRIPT|P|DIV|H1|H2|H3|H4|H5|H6|ADDRESS|PRE|TABLE|TR|TD|TH|INPUT|SELECT|TEXTAREA|OBJECT|A| UL|OL|LI|BASE|META|LINK|HR|BR|PARAM|IMG|AREA|INPUT|SPAN)[^>]*(>?)/ig;
    var Singlable = /BASE|META.|LINK|HR|BR|PARAM|IMG|AREA|INPUT/i;
    var Stack = new Array(), posStack = new Array();
    while (true) {
        var newone = re.exec(Foremost);
        if (newone == null) break;
        if (newone[1] == "") {
            var Elem = newone[2];
            if (Elem.match(Singlable) && newone[3] != "") {
                continue;
            }
            Stack.push(newone[2].toUpperCase());
            posStack.push(newone.index);
            if (newone[3] == "") break;
        } else {
            var StackTop = Stack[Stack.length - 1];
            var End = newone[2].toUpperCase();
            if (StackTop == End) {
                Stack.pop();
                posStack.pop();
                if (newone[3] == "") {
                    Foremost = Foremost + ">";
                }
            }
        };
    }
    var cutpos = posStack.shift();
    Foremost = Foremost.substring(0, cutpos);
    return Foremost;
}
T.length==L
Generate_Brief(T,L)