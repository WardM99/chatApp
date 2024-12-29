package chatapp.dto;

public class Group {
    public int group_id;
    public String name;
    @JsonProperty("private")
    public boolean privateGroup;
}
