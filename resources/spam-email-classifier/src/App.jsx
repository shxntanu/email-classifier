import { useState } from "react";
import axios from "axios";
import { useTypewriter, Cursor } from "react-simple-typewriter";

const App = () => {
  const [spam, setSpam] = useState(false);
  const [loaded, setLoaded] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const subject = formData.get("subject");
    let body = formData.get("body");

    body = "Subject: " + subject + "\n" + body;

    console.log(body);

    try {
      const { data } = await axios.post("http://localhost:8001/predict", {
        email_text: body,
      });
      setLoaded(true);
      setSpam(data.is_spam);
    } catch (err) {
      console.log(err);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    setLoaded(false);
  };

  const [text] = useTypewriter({
    words: ["a spam email !", "a legitimate email !", "well i don't know !"],
    loop: Infinity,
    deleteSpeed: 80,
    delaySpeed: 3000,
  });

  return (
    <div className='h-full w-full bg-[#0D1117] py-10 px-12 md:px-24 lg:px-32'>
      <div className='flex flex-col items-center w-full h-full'>
        <div className='px-8 py-2.5 font-light bg-[#161B22] text-[10px] md:text-[12px] lg:text-[14px] text-[#EEEEEE] rounded-full'>
          Powered by Devently Team
        </div>
        <p className='text-[#F9F8F8] text-center align-middle text-[28px] md:text-[42px] lg:text-[64px] font-bold mt-2'>
          Email Spam Classification
        </p>
        <p className='text-[#848D97] text-[12px] md:text-[14px] lg:text-[18px] font-medium text-center'>
          Say goodbye to unwanted messages cluttering your inbox – let our
          powerfull model help you filter out the noise and prioritize important
          emails.
        </p>
        <div className='flex flex-col ite lg:flex-row w-full h-full mt-4 md:mt-12 lg:mt-16'>
          <div className='flex flex-col text-[24px] md:text-[36px] lg:text-[54px] w-full h-full mt-4'>
            <p className='text-[#F9F8F8] font-bold'>Hello human,</p>
            <p className='text-[#F9F8F8] font-bold'>
              I think this might be,
              <br />
              <span className='text-[#7B61FF] font-bold'>{text}</span>
              <Cursor cursorColor='white' />
            </p>
          </div>
          <div className='w-full'>
            <form onSubmit={handleSubmit} onChange={handleChange}>
              <p className='text-white font-semibold text-[16px] lg:text-[20px] max-lg:mt-12'>
                How to use ?
              </p>
              <p className='text-[#848D97] font-medium text-[12px] md:text-[14px] lg:text-[16px] mt-4'>
                Simply paste or type the content of the email you'd like to
                analyze <br /> in the text input box below and hit the "Predict"
                button !
              </p>
              <input
                type='text'
                id='subject'
                name='subject'
                required
                placeholder='Subject'
                className='w-full bg-slate-800 border border-white font-medium text-gray-100 rounded-lg px-8 py-4 mt-6'
              />
              <textarea
                name='body'
                id='body'
                rows='4'
                required
                placeholder='Enter your email text here...'
                className='w-full bg-slate-800 border border-white font-medium text-gray-100 rounded-lg px-8 py-4 mt-6'
              ></textarea>
              <div className='flex flex-row w-full items-center mt-4 gap-16'>
                <div className='flex-grow'>
                  <button className='bg-[#7B61FF] text-white px-8 py-2 w-fit font-semibold rounded-md'>
                    Predict
                  </button>
                </div>

                {loaded ? (
                  spam ? (
                    <p className='text-red-600 text-[16px] font-medium flex'>
                      This email might be a spam !
                    </p>
                  ) : (
                    <p className='text-green-600 text-[16px] font-medium'>
                      This is a legitimate email !
                    </p>
                  )
                ) : null}
              </div>
            </form>
          </div>
        </div>
        <Cursor />
      </div>
    </div>
  );
};

export default App;
