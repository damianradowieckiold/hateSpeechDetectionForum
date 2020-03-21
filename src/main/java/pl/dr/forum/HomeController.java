package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import pl.dr.forum.repository.TopicRepository;

@Slf4j
@Controller
@RequestMapping("/")
public class HomeController {

    @Autowired
    private TopicRepository repository;

    @GetMapping
    public String startPage(Model model){
        model.addAttribute("topics", repository.getAll());
        return "home";
    }

}
