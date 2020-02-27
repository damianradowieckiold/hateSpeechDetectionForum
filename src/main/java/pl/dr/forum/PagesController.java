package pl.dr.forum;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.ArrayList;
import java.util.List;

@Slf4j
@Controller
public class PagesController {

    @GetMapping("/")
    public String startPage(Model model){
        List<String> topics = new ArrayList<>();
        topics.add("O ptakach");
        topics.add("O drzewach");
        model.addAttribute("topics", topics);
        return "startPage";
    }
}
