import {
  Menubar,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarTrigger,
} from "@/components/ui/menubar";
import { ScrollArea } from "@/components/ui/scroll-area";

import { User } from "@/data/interfaces";
import { logout } from "@/utils/api/user";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { useEffect, useState } from "react";

interface Props {
  user: User;
  setUser: React.Dispatch<React.SetStateAction<User | null>>;
  items: string[];
}

export function MainView({ user, setUser, items }: Props) {
  const [onTop, setOnTop] = useState<boolean>(false)
  function apiLogOut(): void {
    logout();
    setUser(null);
  }

  useEffect(() => {
    if(onTop){
      for(let i = 100; i<105;i++){
        items.push("new message " + i )
      }
      setOnTop(false);
    }

  })

  return (
    <div className="flex flex-col h-screen">
      <Menubar>
        <MenubarMenu>
          <MenubarTrigger>{user.name}</MenubarTrigger>
          <MenubarContent>
            <MenubarItem onClick={apiLogOut}>Log out</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>

      <div className="flex flex-col flex-grow max-h-screen overflow-hidden">
        <ScrollArea
          onScrollTop={() => {
            setOnTop(true);
            console.log("ON TOP");
          }}
          className="flex-grow overflow-y-auto flex-col-reverse"
        >
          <div className="flex flex-col-reverse">
            {items.map((s, index) => (
              <div key={index}>{s}</div>
            ))}
          </div>
        </ScrollArea>

        <div className="flex items-center space-x-2">
          <Input type="text" placeholder="Send message to group" />
          <Button type="submit">Send</Button>
        </div>
      </div>
    </div>
  );
}
