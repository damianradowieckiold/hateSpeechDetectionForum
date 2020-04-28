package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import pl.dr.forum.model.Topic;
import pl.dr.forum.repository.TopicRepository;

import javax.validation.Valid;
import javax.validation.constraints.Size;

@Slf4j
@Controller
@RequestMapping("/")
public class HomeController {

    @Autowired
    private TopicRepository repository;

    @GetMapping
    public String startPage(Model model){
        return toHomePage(model);
    }

    @PostMapping("topic")
    public String addTopic(@Valid Topic newTopic, BindingResult bindingResult, Model model) throws NoSuchFieldException {
        if(!bindingResult.hasErrors()){
            repository.save(newTopic);
        }
        else{
            model.addAttribute("error", retrieveAnnotationMessage(newTopic));
        }
        return toHomePage(model);
    }

    private String retrieveAnnotationMessage(@Valid Topic newTopic) throws NoSuchFieldException {
        return newTopic.getClass().getDeclaredField("name").getDeclaredAnnotation(Size.class).message();
    }

    private String toHomePage(Model model) {
        model.addAttribute("topics", repository.findAll());
        model.addAttribute("newTopic", new Topic());
        return "home";
    }



}
