import { useState } from "react";
import ChatBody from "./components/ChatBody";
import ChatInput from "./components/ChatInput";
import { useMutation } from "react-query";
import { fetchResponse } from "./api";

function App() {
  const [chat, setChat] = useState([]);
  const [active, setActive] = useState(true);
  const [value, setValue] = useState();

  const mutation = useMutation({
    mutationFn: () => {
      return fetchResponse(chat);
    },
    onSuccess: (data) => {
      console.log("API response:", data);
      if (data && data.message) {
        setChat((prev) => [
          ...prev,
          { sender: "ai", message: data.message.replace(/^\n\n/, "") },
        ]);
      } else {
        console.error("API response is missing 'message' property", data);
      }
    },
    onError: (error) => {
      console.error("Mutation error", error);
    }
  });

  const sendMessage = async (message) => {
    await Promise.resolve(setChat((prev) => [...prev, message]));
    mutation.mutate();
  };

  const handleActive = async (message) => {
    console.log("message", message);
    await setActive(message);
    await Promise.resolve(setActive((prev) => message));
  };

  const onClick = (value) => {
    setValue(value);
  };

  return (
    <div className="bg-[#1A232E] h-screen py-6 relative sm:px-16 px-12 text-white overflow-hidden flex flex-col justify-between  align-middle">
      <div className="gradient-01 z-0 absolute"></div>
      <div className="gradient-02 z-0 absolute"></div>

      <div className="uppercase font-bold  text-2xl text-center mb-3">
        Eugene AI doppelgänger
      </div>

      {active ? (
        <div className="w-full max-w-4xl min-w-[20rem] self-center align-middle">
          <div className="row mb-3">
            <div className="w-full max-w-4xl min-w-[20rem] self-center text-center">
              <p>
                Hello, I'm Eugene doppelgänger. <br />
                An highly intelligent chatbot that can answer questions about Eugene's past experiences, career goals, and more.<br /><br />
                If you wish to schedule an interview with me in person,<br />
                please reach me @ +65 9145 9415<br /><br />
              </p>
            </div>
          </div>
          <div class="h-24 md:flex items-start text-center gap-3.5">
            <div class="h-full flex flex-col mb-8 md:mb-auto gap-3.5 flex-1">
              <ul class="h-full flex flex-col gap-3.5 w-full sm:max-w-md m-auto">
                <button
                  class="h-full bg-transparent hover:bg-white text-white-700 font-semibold hover:text-blue-500 py-2 px-4 border border-blue-500 hover:border-transparent rounded"
                  onClick={() => {
                    onClick("Tell me more about yourself");
                  }}
                >
                  Tell me more about yourself
                  <br />
                  →
                </button>
              </ul>
            </div>
            <div class="h-24 flex flex-col mb-8 md:mb-auto gap-3.5 flex-1">
              <ul class="h-full flex flex-col gap-3.5 w-full sm:max-w-md m-auto">
                <button
                  class="h-full bg-transparent hover:bg-white text-white-700 font-semibold hover:text-blue-500 py-2 px-4 border border-blue-500 hover:border-transparent rounded"
                  onClick={() => {
                    onClick(
                      "What are your biggest accomplishments?"
                    );
                  }}
                >
                  What are your biggest accomplishments?
                  <br />
                  →
                </button>
              </ul>
            </div>
            <div class="h-24 flex flex-col mb-8 md:mb-auto gap-3.5 flex-1">
              <ul class="h-full flex flex-col gap-3.5 w-full sm:max-w-md m-auto">
                <button
                  class="h-full bg-transparent hover:bg-white text-white-700 font-semibold hover:text-blue-500 py-2 px-4 border border-blue-500 hover:border-transparent rounded"
                  onClick={() => {
                    onClick("What are your career goals?");
                  }}
                >
                  What are your career goals?
                  <br />
                  →
                </button>
              </ul>
            </div>
          </div>
        </div>
      ) : null}

      <div
        className="h-[90%] overflow-auto w-full max-w-4xl min-w-[20rem] py-8 px-4 self-center
      scrollbar-thumb-slate-400 scrollbar-thin scrollbar-track-gray-tranparent scrollbar-thumb-rounded-md
      "
      >
        <ChatBody chat={chat} />
      </div>

      <div className="w-full max-w-4xl min-w-[20rem] self-center">
        <ChatInput
          sendMessage={sendMessage}
          loading={mutation.isLoading}
          defaultSearch={value}
          setActive={setActive}
        />
      </div>
    </div>
  );
}

export default App;